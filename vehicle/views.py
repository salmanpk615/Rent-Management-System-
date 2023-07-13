from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, CreateView

# Create your views here.
from vehicle.forms import PassengerForm, PassengerUpdateForm
from vehicle.models import Vehicle, VehicleProvider, Passenger


def home(request):
    return render(request, 'vehicle/home.html')


# Vehicles List
class VehicleListView(ListView):

    model = Vehicle
    template_name = "vehicle/vehicle.html"


# Passengers Detail
class PassengerDetailView(DetailView):
    model = Vehicle
    template_name = "vehicle/passenger.html"

    def get_context_data(self, **kwargs):
        context = super(PassengerDetailView, self).get_context_data(**kwargs)
        context['form'] = PassengerForm
        return context


# Add Passenger
class PassengerCreateView(CreateView):
    model = Passenger
    template_name = "vehicle/passenger_create.html"
    form_class = PassengerForm

    def form_valid(self, form):
        form.instance.vehicle_id = self.kwargs['pk']
        form.save()
        data = {
            'id': form.instance.id,
            'full_name': form.instance.full_name,
            'phone_number': form.instance.phone_number,
            'joining_date': form.instance.joining_date.strftime('%b. %d, %Y'),
            'gender': form.instance.get_gender_display(),
            'rent_type': form.instance.get_rent_type_display(),
            'fix_rent': form.instance.fix_rent,
        }
        return JsonResponse({'data': data}, status=200)

    def form_invalid(self, form):
        return JsonResponse({"errors": dict(form.errors)}, status=400)


# Update/Edit Passenger
class PassengerUpdateView(UpdateView):
    model = Passenger
    form_class = PassengerUpdateForm

    # def get_success_url(self):
    #     return reverse('passenger', kwargs={'pk': self.object.vehicle_id})

    def get(self, request, *args, **kwargs):
        passenger = self.get_object(self.get_queryset())
        data = {
            'full_name': passenger.full_name,
            'phone_number': passenger.phone_number,
            'joining_date': passenger.joining_date,
            'gender': passenger.gender,
            'rent_type': passenger.rent_type,
            'fix_rent': passenger.fix_rent,
        }
        return JsonResponse(data, status=200)

    def form_valid(self, form):
        form.save()
        data = {
            'id': form.instance.id,
            'full_name': form.instance.full_name,
            'phone_number': form.instance.phone_number,
            'joining_date': form.instance.joining_date.strftime('%b. %d, %Y'),
            'gender': form.instance.get_gender_display(),
            'rent_type': form.instance.get_rent_type_display(),
            'fix_rent': form.instance.fix_rent,
        }
        return JsonResponse({'data': data}, status=200)

    def form_invalid(self, form):
        return JsonResponse({"errors": dict(form.errors)}, status=400)


# Delete Passenger
class PassengerDeleteView(DeleteView):
    model = Passenger
    template_name = "vehicle/passenger_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle_id'] = self.object.vehicle_id
        return context

    def get_success_url(self):
        return reverse('passenger', kwargs={'pk': self.object.vehicle_id})
