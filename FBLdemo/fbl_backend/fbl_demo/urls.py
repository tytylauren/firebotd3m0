# fbl_demo/urls.py
from django.urls import path
from .views import DroneListCreateView, launch_simulation

urlpatterns = [
    path('drones/', DroneListCreateView.as_view(), name='drone-list-create'),
    path('launch_simulation/', launch_simulation, name='launch_simulation'),
]

