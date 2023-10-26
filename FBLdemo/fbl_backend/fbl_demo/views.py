from django.shortcuts import render
from rest_framework import generics
from .models import Drone
from .serializers import DroneSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import subprocess

@csrf_exempt
class DroneListCreateView(generics.ListCreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer


@csrf_exempt
def launch_simulation(request):
   

    if request.method == "POST":
        subprocess.Popen(["/home/firebot/FBLProjects/FBLdemo/fbl_backend/launch.sh"], close_fds=True)
        return JsonResponse({"status": "Simulation started"})
   
