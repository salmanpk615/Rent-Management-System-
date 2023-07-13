from django.forms import ModelForm
from expense.models import Rent, Expense, LocalRent
from vehicle.rent_generate import generate_rent


# Rent Generate
class RentForm(ModelForm):
    class Meta:
        model = Rent
        fields = ['expense_month', 'year']

    def save(self, commit=True):
        instance = super(RentForm, self).save(commit=True)
        vehicle_obj = instance.vehicle
        generate_rent(instance, vehicle_obj)


# Adding Rent Form
class ExpenseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
        self.fields["amount"].widget.attrs["placeholder"] = "Enter Amount Here"
        self.fields["date"].widget.attrs["placeholder"] = "YYYY-MM-DD"
        self.fields["expense_type"].widget.attrs["placeholder"] = "choose an option"

    class Meta:
        model = Expense
        exclude = ['vehicle']


# Adding LocalRent Form
class LocalRentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
        self.fields["local_rent"].widget.attrs["placeholder"] = "Enter Local Rent Here"
        self.fields["date"].widget.attrs["placeholder"] = "YYYY-MM-DD"

    class Meta:
        model = LocalRent
        exclude = ['vehicle']


# Adding Rent Form
class RentsForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
        self.fields["expense_month"].widget.attrs["placeholder"] = "choose an option"

    class Meta:
        model = Rent
        exclude = ['vehicle', 'rent', 'total_expense_vehicle', 'total_expense_provider', 'total_local_rent',
                   'final_rent']

    def save(self, commit=True):
        instance = super(RentsForm, self).save(commit=True)
        vehicle_obj = instance.vehicle
        generate_rent(instance, vehicle_obj)


# Update/Edit Expense Form
class ExpenseUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
        self.fields["amount"].widget.attrs["placeholder"] = "Enter Amount Here"
        self.fields["date"].widget.attrs["placeholder"] = "YYYY-MM-DD"
        self.fields["expense_type"].widget.attrs["placeholder"] = "choose an option"

    class Meta:
        model = Expense
        exclude = ['vehicle']


# Update/Edit LocalRent Form
class LocalRentUpdateFrom(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
        self.fields["local_rent"].widget.attrs["placeholder"] = "Enter Local Rent Here"
        self.fields["date"].widget.attrs["placeholder"] = "YYYY-MM-DD"

    class Meta:
        model = LocalRent
        exclude = ['vehicle']
