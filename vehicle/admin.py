from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html

from vehicle.models import VehicleProvider, Vehicle, Passenger


class PassengerAdmin(admin.TabularInline):
    model = Passenger


class VehicleList(admin.ModelAdmin):
    list_display = ('bar', 'name', 'vehicle_number', 'model_number',
                    'capacity', 'color', 'monthly_rent', 'vehicle_provider')

    # def Add_Passenger(self, obj):
    #     add_url = f"{reverse('admin:vehicle_passenger_add')}?vehicle={obj.id}"
    #     return format_html("<a href='%s'>Add Passenger</a>" % add_url)

    inlines = (
        PassengerAdmin,
    )

    def bar(self, obj):
        return format_html(f"<img src='{obj.image.url}' style='width:40px;height:40px;'")

    # bar.short_description = 'image'


class ProviderList(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'address')


# class PassengerList(admin.ModelAdmin):
#     list_display = ('full_name', 'phone_number', 'joining_date',
#                     'gender', 'rent_type', 'fix_rent', 'vehicle')


admin.site.register(VehicleProvider, ProviderList)
admin.site.register(Vehicle, VehicleList)
# admin.site.register(Passenger, PassengerAdmin)

