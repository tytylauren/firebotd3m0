from django.urls import path
from . import views

urlpatterns = [
    path('launch_simulation/', views.launch_simulation, name='launch_simulation'),
]
