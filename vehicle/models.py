from django.contrib.auth.models import User

from django.db import models

# Create your models here.


Gender_CHOICE = (
    ('male', 'male'),
    ('female', 'female'),
    ('another', 'another')
)


class VehicleProvider(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=50)
    vehicle_number = models.CharField(max_length=50)
    model_number = models.CharField(max_length=50)
    capacity = models.IntegerField()
    color = models.CharField(max_length=50)
    image = models.ImageField(upload_to='image')
    monthly_rent = models.IntegerField()
    vehicle_provider = models.ForeignKey(VehicleProvider, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Passenger(models.Model):
    CHOICE = (
        ('One sided', 'One sided'),
        ('Two sided', 'Two sided'),
        ('Fix rent', 'Fix rent')
    )
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    joining_date = models.DateField(auto_now_add=True)
    gender = models.CharField(max_length=10, choices=Gender_CHOICE)
    rent_type = models.CharField(max_length=10, choices=CHOICE)
    fix_rent = models.IntegerField(default=0)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['-id']
