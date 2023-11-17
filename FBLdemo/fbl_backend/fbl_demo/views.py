# views.py
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .models import Drone
from .serializers import DroneSerializer
import subprocess
import asyncio
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


from .pymavlink import (check_ground_station_status, get_mission, arm_drone as pymavlink_arm_drone, 
                        disarm_drone as pymavlink_disarm_drone, start_mission, pause_mission, end_mission, get_telemetry_data)
from .mavsdk import (connect_drone, get_drone_state, get_battery_status, get_gps_info, get_flight_mode, 
                     get_home_position, get_in_air_status, get_health_status, get_velocity, 
                     arm_drone as mavsdk_arm_drone, disarm_drone as mavsdk_disarm_drone, takeoff_drone, land_drone)



def run_async(func, *args):
    return asyncio.run(func(*args))

class DroneListCreateView(generics.ListCreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer

@csrf_exempt
@require_http_methods(["POST"])
def launch_simulation(request):
    try:
        subprocess.Popen(["/home/firebot/FBLProjects/FBLdemo/fbl_backend/launch.sh"], close_fds=True)
        return JsonResponse({"status": "Simulation started"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
        
@csrf_exempt
def drone_telemetry(request):
    try:
        # Connect to the drone asynchronously
        drone = run_async(connect_drone)

        # Fetch battery status, GPS info, and flight mode asynchronously
        battery = run_async(get_battery_status, drone)
        gps_info = run_async(get_gps_info, drone)
        flight_mode = run_async(get_flight_mode, drone)

        # Aggregate the data into a response
        response_data = {
            "battery": battery.remaining_percent * 100,
            "gps_info": {"lat": gps_info.latitude_deg, "lon": gps_info.longitude_deg},
            "flight_mode": flight_mode.name
        }

        # Send the response back to the client
        return JsonResponse(response_data)

    except Exception as e:
        # Handle any errors that occur during the process
        return HttpResponseServerError({"error": str(e)})


@require_http_methods(["GET"])
def ground_station_status(request):
    try:
        status = check_ground_station_status()
        return JsonResponse({"ground_station_status": status})
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})

@require_http_methods(["GET"])
def drone_connection_status(request):
    try:
        drone = run_async(connect_drone)
        state = run_async(get_drone_state, drone)
        return JsonResponse({"connection_status": state})
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})

@require_http_methods(["POST"])
def arm_drone_mavsdk(request):
    try:
        drone = run_async(connect_drone)
        run_async(mavsdk_arm_drone, drone)
        return JsonResponse({"status": "Drone armed with mavsdk"})
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})

@require_http_methods(["POST"])
def disarm_drone_mavsdk(request):
    try:
        drone = run_async(connect_drone)
        run_async(mavsdk_disarm_drone, drone)
        return JsonResponse({"status": "Drone disarmed with mavsdk"})
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})

@require_http_methods(["POST"])
def takeoff_drone_mavsdk(request):
    try:
        drone = run_async(connect_drone)
        run_async(takeoff_drone, drone)
        return JsonResponse({"status": "Drone taking off with mavsdk"})
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})

@require_http_methods(["POST"])
def land_drone_mavsdk(request):
    try:
        drone = run_async(connect_drone)
        run_async(land_drone, drone)
        return JsonResponse({"status": "Drone landing with mavsdk"})
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})

@require_http_methods(["POST"])
def arm_drone_pymavlink(request):
    try:
        pymavlink_arm_drone()
        return JsonResponse({"status": "Drone armed with pymavlink"})
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})

@require_http_methods(["POST"])
def disarm_drone_pymavlink(request):
    try:
        pymavlink_disarm_drone()
        return JsonResponse({"status": "Drone disarmed with pymavlink"})
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})

@require_http_methods(["POST"])
def start_mission_pymavlink(request):
    try:
        start_mission()
        return JsonResponse({"status": "Mission started with pymavlink"})
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})

@require_http_methods(["POST"])
def pause_mission_pymavlink(request):
    try:
        pause_mission()
        return JsonResponse({"status": "Mission paused with pymavlink"})
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})

@require_http_methods(["POST"])
def end_mission_pymavlink(request):
    try:
        end_mission()
        return JsonResponse({"status": "Mission ended with pymavlink"})
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})

@require_http_methods(["GET"])
def get_telemetry(request):
    try:
        telemetry_data = get_telemetry_data()
        return JsonResponse({"telemetry": telemetry_data})
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})

@require_http_methods(["GET"])
def get_battery_status_view(request):
    try:
        drone = run_async(connect_drone)
        battery_status = run_async(get_battery_status, drone)
        return JsonResponse({"battery_status": battery_status.remaining_percent * 100})
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})

@require_http_methods(["GET"])
def get_gps_info_view(request):
    try:
        drone = run_async(connect_drone)
        gps_info = run_async(get_gps_info, drone)
        return JsonResponse({"gps_info": {"latitude": gps_info.latitude_deg, "longitude": gps_info.longitude_deg}})
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})



@csrf_exempt
@require_http_methods(["POST"])
def update_drone_status(request):
    try:
        # Extract data from request (e.g., new status)
        data = json.loads(request.body)
        new_status = data.get('status', 'Unknown') 
        drone_id = data.get('drone_id')
        if drone_id:
            drone = Drone.objects.get(id=drone_id)
            drone.status = new_status
            drone.save()
            status_message = f"Drone {drone_id} status updated to {new_status}"
        else:
            status_message = "Drone ID not provided"

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "drone_operations",
            {
                "type": "broadcast_message",
                "message": status_message
            }
        )
        
        return JsonResponse({"status": status_message})
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def update_drone_location(request):
    try:
        data = json.loads(request.body)
        drone_id = data.get('drone_id')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if drone_id and latitude is not None and longitude is not None:
            drone = Drone.objects.get(id=drone_id)
            drone.latitude = latitude
            drone.longitude = longitude
            drone.save()
            return JsonResponse({"status": f"Drone {drone_id} location updated"})
        else:
            return HttpResponseServerError({"error": "Missing data"})
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})


@csrf_exempt
@require_http_methods(["GET"])
def get_drone_information(request, drone_id):
    try:
        drone = Drone.objects.get(id=drone_id)
        data = {
            "id": drone.id,
            "status": drone.status,
            "latitude": drone.latitude,
            "longitude": drone.longitude
            # Add more fields as needed
        }
        return JsonResponse(data)
    except Drone.DoesNotExist:
        return JsonResponse({"error": "Drone not found"}, status=404)
    except Exception as e:
        return HttpResponseServerError({"error": str(e)})
        
        


