from django.contrib.auth.models import User

from django.db import models

# Create your models here.
from vehicle.models import Vehicle, Passenger

CHOICE = (
    ('Paid', 'Paid'),
    ('Not Paid', 'Not Paid')
)

EXPENSE_CHOICE = (
    ('provider_expense', 'provider_expense'),
    ('vehicle_expense', 'vehicle_expense')
)

RENT_CHOICE = (
    ('one sided', 'one sided'),
    ('two sided', 'two sided'),
    ('fix rent', 'fix rent')
)

MONTH_CHOICE = (
    (1, 'january'),
    (2, 'february'),
    (3, 'march'),
    (4, 'april'),
    (5, 'may'),
    (6, 'june'),
    (7, 'july'),
    (8, 'august'),
    (9, 'september'),
    (10, 'october'),
    (11, 'november'),
    (12, 'december')
)


class Rent(models.Model):
    expense_month = models.IntegerField(choices=MONTH_CHOICE)
    year = models.CharField(max_length=50)
    rent = models.PositiveIntegerField(default=0)
    total_expense_provider = models.IntegerField(default=0)
    total_expense_vehicle = models.IntegerField(default=0)
    total_local_rent = models.IntegerField(default=0)
    final_rent = models.IntegerField(default=0)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __int__(self):
        return int(self.expense_month)


class Expense(models.Model):
    expense_type = models.CharField(max_length=20, choices=EXPENSE_CHOICE)
    amount = models.IntegerField()
    date = models.DateField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __int__(self):
        return int(self.amount)

    class Meta:
        ordering = ['-date']


class LocalRent(models.Model):
    local_rent = models.IntegerField()
    date = models.DateField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __int__(self):
        return int(self.local_rent)


class RentDetail(models.Model):
    total_rent = models.IntegerField()
    rent_type = models.CharField(max_length=50, choices=RENT_CHOICE)
    status = models.CharField(max_length=50, choices=CHOICE, default='Not Paid')
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE)

    def __int__(self):
        return int(self.total_rent)
