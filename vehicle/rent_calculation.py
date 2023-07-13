from django.db.models import Sum, Q, Count

from expense.models import Rent, LocalRent, Expense
from vehicle.models import Vehicle


def calculation(id, expense_month):
    vehicle = Vehicle.objects.get(id=id)
    passenger = LocalRent.objects.filter(vehicle_id=id, date__month=expense_month)
    local_rent = passenger.aggregate(local_rent=Sum('local_rent', default=0))

    exp = Expense.objects.filter(vehicle_id=id, date__month=expense_month)
    total_expense = exp.aggregate(
        vehicle_expense=Sum('amount', filter=Q(expense_type='vehicle_expense'), default=0),
        provider_expense=Sum('amount', filter=Q(expense_type='provider_expense'), default=0)

    )

    rent = vehicle.monthly_rent + total_expense['vehicle_expense'] \
           - local_rent['local_rent'] - total_expense['provider_expense']

    # return local_rent['local_rent'], total_expense['vehicle_expense'], total_expense['provider_expense']

    passengers = vehicle.passenger_set.aggregate(
        onesided=Count('id', filter=Q(rent_type='One sided')),
        twosided=Count('id', filter=Q(rent_type='Two sided')),
        fixrentp=Count('id', filter=Q(rent_type='Fix rent')),
        fixrent=Sum('fix_rent', filter=Q(rent_type='Fix rent'), default=0),
        all=Count('id')

    )

    rent -= passengers['fixrent']
    passengers['all'] -= passengers['fixrentp']
    per_side_rent = (((100 / (passengers['all'] * 2)) / 100) * rent)
    one_sided_rent = per_side_rent
    two_sided_rent = per_side_rent * 2
    remaining = rent - ((one_sided_rent * passengers['onesided']) + (two_sided_rent * passengers['twosided']))
    extra = remaining / passengers['all']
    one_sided_rent += extra
    two_sided_rent += extra

    return round(one_sided_rent, 0), round(two_sided_rent, 0), \
           local_rent['local_rent'], total_expense['vehicle_expense'], total_expense['provider_expense'], \
           passengers['fixrent'], passengers['fixrentp']