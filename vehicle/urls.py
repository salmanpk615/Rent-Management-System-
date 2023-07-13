from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('vehicle', views.VehicleListView.as_view(), name='vehicle'),
    path('passenger/<int:pk>', views.PassengerDetailView.as_view(), name='passenger'),
    path('passenger_create/<int:pk>', views.PassengerCreateView.as_view(), name='passenger_create'),
    path('passenger_update/<int:pk>', views.PassengerUpdateView.as_view(), name='passenger_update'),
    path('passenger_delete/<int:pk>', views.PassengerDeleteView.as_view(), name='passenger_delete'),
]
