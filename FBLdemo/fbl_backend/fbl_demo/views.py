# views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .models import Drone
from .serializers import DroneSerializer
import subprocess

class DroneListCreateView(generics.ListCreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer

@csrf_exempt
@require_POST
def launch_simulation(request):
    try:
        subprocess.Popen(["/home/firebot/FBLProjects/FBLdemo/fbl_backend/launch.sh"], close_fds=True)
        return JsonResponse({"status": "Simulation started"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

