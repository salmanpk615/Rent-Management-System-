from expense.models import RentDetail
from vehicle.rent_calculation import calculation


def generate_rent(obj, vehicle):
    """Generate rent for a vehicle."""
    obj.rent = vehicle.monthly_rent
    one_sided_rent, two_sided_rent, total_local_rent, total_expense_vehicle, total_expense_provider, \
    passengers_fixrent, passengers_fixrentp = calculation(
        id=vehicle.id,
        expense_month=obj.expense_month
    )
    obj.total_local_rent = total_local_rent
    obj.total_expense_vehicle = total_expense_vehicle
    obj.total_expense_provider = total_expense_provider
    obj.final_rent = obj.rent + passengers_fixrent + total_expense_vehicle - (
            obj.total_local_rent + obj.total_expense_provider + passengers_fixrent)
    obj.save()
    for passenger in vehicle.passenger_set.all():
        exp = RentDetail(rent=obj)
        if passenger.rent_type == "One sided":
            exp.rent_type = "one sided"
            exp.total_rent = one_sided_rent
        elif passenger.rent_type == "Two sided":
            exp.total_rent = two_sided_rent
            exp.rent_type = "two sided"
        else:
            exp.rent_type = "Fix rent"
            exp.total_rent = passenger.fix_rent
        exp.passenger = passenger
        exp.save()
