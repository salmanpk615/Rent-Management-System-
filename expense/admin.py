from django.contrib import admin

# Register your models here.
from expense.models import Rent, Expense, LocalRent, RentDetail
from vehicle.rent_calculation import calculation


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('expense_type', 'amount', 'date', 'vehicle')


class RentDetailAdmin(admin.TabularInline):
    model = RentDetail
    extra = 0
    readonly_fields = ['passenger', 'rent_type', 'total_rent']

    def has_add_permission(self, request, obj):
        return False


class RentAdmin(admin.ModelAdmin):
    exclude = ('rent', 'total_expense_provider', 'total_expense_vehicle', 'total_local_rent', 'final_rent')
    list_display = ("vehicle", 'expense_month', 'year', 'rent', 'total_expense_provider',
                    'total_expense_vehicle', 'total_local_rent', 'final_rent',)

    inlines = (
        RentDetailAdmin,
    )

    def save_model(self, request, obj, form, change):
        if change:
            return super(RentAdmin, self).save_model(request, obj, form, change)
        vehicle_obj = obj.vehicle
        obj.rent = vehicle_obj.monthly_rent

        one_sided_rent, two_sided_rent, total_local_rent, total_expense_vehicle, total_expense_provider, \
        passengers_fixrent, passengers_fixrentp = calculation(
            id=vehicle_obj.id,
            expense_month=obj.expense_month
        )

        obj.total_local_rent = total_local_rent
        obj.total_expense_provider = total_expense_provider
        obj.total_expense_vehicle = total_expense_vehicle
        obj.final_rent = obj.rent + passengers_fixrent + total_expense_vehicle - \
                         (obj.total_local_rent + obj.total_expense_provider + passengers_fixrent)
        obj.save()
        for passenger in vehicle_obj.passenger_set.all():
            exp = RentDetail(rent=obj)
            if passenger.rent_type == "One sided":
                exp.rent_type = "one sided"
                exp.total_rent = one_sided_rent
            elif passenger.rent_type == "Two sided":
                exp.total_rent = two_sided_rent
                exp.rent_type = "two sided"
            else:
                exp.rent_type = "fix rent"
                exp.total_rent = passenger.fix_rent
            exp.passenger = passenger
            exp.save()


class LocalRentAdmin(admin.ModelAdmin):
    list_display = ('local_rent', 'date', 'vehicle')


# class RentDetailAdmin(admin.ModelAdmin):
#     list_display = ('total_rent', 'rent_type', 'status', 'passenger', 'rent')


admin.site.register(Rent, RentAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(LocalRent, LocalRentAdmin)
# admin.site.register(RentDetail, RentDetailAdmin)
