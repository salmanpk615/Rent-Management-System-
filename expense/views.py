from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from expense.forms import RentForm, ExpenseForm, LocalRentForm, RentsForm, ExpenseUpdateForm, LocalRentUpdateFrom
from expense.models import Expense, RentDetail, Rent, LocalRent
from vehicle.models import Vehicle
from vehicle.rent_calculation import calculation


# Expense Detail
class ExpenseDetailView(DetailView):
    model = Vehicle
    template_name = "expense/expense.html"

    def get_context_data(self, **kwargs):
        context = super(ExpenseDetailView, self).get_context_data(**kwargs)
        context['form'] = ExpenseForm
        return context


# Add Expense
class ExpenseCreateView(CreateView):
    model = Expense
    template_name = "expense/expense_create.html"
    form_class = ExpenseForm

    def form_valid(self, form):
        form.instance.vehicle_id = self.kwargs['pk']
        form.save()
        data = {
            # 'id': form.instance.id,
            'expense_type': form.instance.expense_type,
            'amount': form.instance.amount,
            'date': form.instance.date.strftime('%b. %d, %Y'),
            'vehicle_name': form.instance.vehicle.name,
        }
        return JsonResponse({'data': data}, status=200)

    def form_invalid(self, form):
        return JsonResponse({'errors': dict(form.errors)}, status=400)


# Update/Edit Expense
class ExpenseUpdateView(UpdateView):
    model = Expense
    # template_name = "expense/expense_update.html"
    form_class = ExpenseUpdateForm

    # def get_success_url(self):
    #     return reverse('expense', kwargs={'pk': self.object.vehicle_id})

    def get(self, request, *args, **kwargs):
        expense = self.get_object(self.get_queryset())
        data = {
            'id': expense.id,
            'expense_type': expense.expense_type,
            'amount': expense.amount,
            'date': expense.datestrftime('%b. %d, %Y'),
        }
        return JsonResponse(data, status=200)

    def form_valid(self, form):
        form.save()
        data = {
            'id': form.instance.id,
            'expense_type': form.instance.expense_type,
            'amount': form.instance.amount,
            'date': form.instance.date.strftime('%b. %d, %Y'),
            'vehicle_name': form.instance.vehicle.name,
        }
        return JsonResponse({'data': data}, status=200)

    def form_invalid(self, form):
        return JsonResponse({'errors': dict(form.errors)}, status=400)


# Delete Expense
class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = "expense/expense_delete.html"

    def get_context_data(self, **kwargs):
        context = super(ExpenseDeleteView, self).get_context_data(**kwargs)
        context['vehicle_id'] = self.object.vehicle_id
        return context

    def get_success_url(self):
        return reverse('expense', kwargs={'pk': self.object.vehicle_id})


# All Rents
class RentDetailView(DetailView):
    model = Vehicle
    template_name = "expense/rent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RentsForm
        context['vehicle'] = get_object_or_404(Vehicle, pk=self.kwargs['pk'])
        return context


# Rent Detail
class RentListView(ListView):
    model = RentDetail
    template_name = "expense/rent_list.html"

    def get_queryset(self):
        super(RentListView, self).get_queryset()
        queryset = RentDetail.objects.filter(rent_id=self.kwargs['pk'])
        return queryset


# Add Rent
class RentCreateView(CreateView):
    model = Rent
    template_name = "expense/rent_create.html"
    # form_class = RentForm
    form_class = RentsForm

    def form_valid(self, form):
        form.instance.vehicle_id = self.kwargs['pk']
        form.save()
        data = {
            'expense_month': form.instance.get_expense_month_display(),
            'year': form.instance.year,
            'rent': form.instance.rent,
            'total_expense_provider': form.instance.total_expense_provider,
            'total_expense_vehicle': form.instance.total_expense_vehicle,
            'total_local_rent': form.instance.total_local_rent,
            'final_rent': form.instance.final_rent,
            'vehicle_name': form.instance.vehicle.name,
        }
        return JsonResponse({'data': data}, status=200)

    def form_invalid(self, form):
        return JsonResponse({'errors': dict(form.errors)}, status=400)


# Delete Rent
class RentDeleteView(DeleteView):
    model = Rent
    template_name = "expense/rent_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle_id'] = self.object.vehicle_id
        return context

    def get_success_url(self):
        return reverse('rent', kwargs={'pk': self.object.vehicle_id})


# Local Rent Details
class LocalRentDetailView(DetailView):
    model = Vehicle
    template_name = "expense/local_rent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LocalRentForm
        return context


# Add Local Rent
class LocalRentCreateView(CreateView):
    model = LocalRent
    # template_name = "expense/local_rent_create.html"
    form_class = LocalRentForm

    def form_valid(self, form):
        form.instance.vehicle_id = self.kwargs['pk']
        form.save()
        data = {
            'local_rent': form.instance.local_rent,
            'date': form.instance.date.strftime('%b. %d, %Y'),
            'id': form.instance.id,
        }
        return JsonResponse(data, status=200)

    def form_invalid(self, form):
        return JsonResponse({'errors': dict(form.errors)}, status=400)


# Update/Edit Local Rent
class LocalRentUpdateView(UpdateView):
    model = LocalRent
    # template_name = "expense/local_rent_update.html"
    form_class = LocalRentUpdateFrom

    # def get_success_url(self):
    #     return reverse('local_rent', kwargs={'pk': self.object.vehicle_id})

    def get(self, request, *args, **kwargs):
        local_rent = self.get_object(self.get_queryset())
        data = {
            'id': local_rent.id,
            'local_rent': local_rent.local_rent,
            'date': local_rent.date.strftime('%b. %d, %Y'),
        }
        return JsonResponse(data, status=200)

    def form_valid(self, form):
        form.save()
        data = {
            'id': form.instance.id,
            'local_rent': form.instance.local_rent,
            'date': form.instance.date.strftime('%b. %d, %Y'),
        }
        return JsonResponse(data, status=200)

    def form_invalid(self, form):
        return JsonResponse({'errors': dict(form.errors)}, status=400)


# Delete Local Rent
class LocalRentDeleteView(DeleteView):
    model = LocalRent
    template_name = "expense/local_rent_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['vehicle_id'] = self.object.vehicle_id
        return context

    def get_success_url(self):
        return reverse('local_rent', kwargs={'pk': self.object.vehicle_id})
