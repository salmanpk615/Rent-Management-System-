from django.urls import path

from . import views

urlpatterns = [
    path('expense/<int:pk>', views.ExpenseDetailView.as_view(), name='expense'),
    path('rent/<int:pk>', views.RentDetailView.as_view(), name='rent'),
    path('local_rent/<int:pk>', views.LocalRentDetailView.as_view(), name='local_rent'),
    path('expense_create/<int:pk>', views.ExpenseCreateView.as_view(), name='expense_create'),
    path('rent_create/<int:pk>', views.RentCreateView.as_view(), name='rent_create'),
    path('rent_delete/<int:pk>', views.RentDeleteView.as_view(), name='rent_delete'),
    path('local_rent_create/<int:pk>', views.LocalRentCreateView.as_view(), name='local_rent_create'),
    path('expense_update/<int:pk>', views.ExpenseUpdateView.as_view(), name='expense_update'),
    path('expense_delete/<int:pk>', views.ExpenseDeleteView.as_view(), name='expense_delete'),
    path('local_rent_update/<int:pk>', views.LocalRentUpdateView.as_view(), name='local_rent_update'),
    path('local_rent_delete/<int:pk>', views.LocalRentDeleteView.as_view(), name='local_rent_delete'),
    path('rent_list/<int:pk>', views.RentListView.as_view(), name='rent_list'),

]
