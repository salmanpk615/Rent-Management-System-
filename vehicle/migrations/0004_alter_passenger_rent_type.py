# Generated by Django 4.1 on 2022-08-30 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0003_alter_passenger_gender_alter_passenger_rent_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passenger',
            name='rent_type',
            field=models.CharField(choices=[('One sided', 'One sided'), ('Two sided', 'Two sided')], max_length=10),
        ),
    ]
