from django.forms import ModelForm

from vehicle.models import Passenger


class PassengerForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
        self.fields["full_name"].widget.attrs["placeholder"] = "Enter Your Name Here"
        self.fields["phone_number"].widget.attrs["placeholder"] = "0-9"
        self.fields["gender"].widget.attrs["placeholder"] = "choose an option"
        self.fields["rent_type"].widget.attrs["placeholder"] = "choose an option"
        self.fields["fix_rent"].widget.attrs["placeholder"] = "0"

    class Meta:
        model = Passenger
        exclude = ['vehicle', 'joining_date']


class PassengerUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
        self.fields["full_name"].widget.attrs["placeholder"] = "Enter Your Name Here"
        self.fields["phone_number"].widget.attrs["placeholder"] = "0-9"
        self.fields["gender"].widget.attrs["placeholder"] = "choose an option"
        self.fields["rent_type"].widget.attrs["placeholder"] = "choose an option"
        self.fields["fix_rent"].widget.attrs["placeholder"] = "0"

    class Meta:
        model = Passenger
        exclude = ['vehicle', 'joining_date']


