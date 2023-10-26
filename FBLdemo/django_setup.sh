#!/bin/bash

sudo apt update -y

cd DjangoFBL

echo "from mavsdk import System
import asyncio
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from random import uniform
from mavsdk.mission import (MissionItem, MissionPlan)
from asgiref.sync import async_to_sync
from django.shortcuts import render

async def video_feed(request):
    return render(request, 'video_feed.html')

async def connect_drone():
    drone = System()
    await drone.connect(system_address="udp://:14540")
    return drone

async def get_drone_info(drone):
    info = await drone.info.get_version()
    return {
        "Flight stack version": info.flight_sw_version,
        "Flight stack vendor": info.flight_vendor_major,
    }
    
async def get_live_coordinates(drone):
    async for position in drone.telemetry.position():
        return {
            "latitude": position.latitude_deg,
            "longitude": position.longitude_deg,
            "absolute_altitude": position.absolute_altitude_m,
            "relative_altitude": position.relative_altitude_m
        }
        
async def start_mission(drone):
    
    # Generate random coordinates for the mission
    latitude = uniform(-90, 90)
    longitude = uniform(-180, 180)
    altitude = uniform(10, 100)
    
    mission_items = [MissionItem(latitude, longitude, altitude, 0, 0, 0, 0, 0, 0, 0)]
    mission_plan = MissionPlan(mission_items)
    
    await drone.mission.upload_mission(mission_plan)
    await drone.mission.start_mission()

async def pause_mission(drone):
    # Add your pause logic here
    return {"status": "Mission paused"}

async def resume_mission(drone):
    # Add your resume logic here
    return {"status": "Mission resumed"}

async def return_to_base(drone):
    # Add your return logic here
    return {"status": "Returning to base"}
    
@csrf_exempt
def connect_to_drone_view(request):
    if request.method == 'POST':
        loop = asyncio.get_event_loop()
        drone = loop.run_until_complete(connect_drone())
        drone_info = loop.run_until_complete(get_drone_info(drone))
        return JsonResponse(drone_info)

@csrf_exempt
def live_coordinates_view(request):
    if request.method == 'GET':
        loop = asyncio.get_event_loop()
        drone = loop.run_until_complete(connect_drone())
        coordinates = loop.run_until_complete(get_live_coordinates(drone))
        return JsonResponse(coordinates)

        
@csrf_exempt
def start_mission_view(request):
    async_to_sync(start_mission)()
    return JsonResponse({'status': 'Mission started'})


@csrf_exempt
def pause_mission_view(request):
    if request.method == 'POST':
        loop = asyncio.get_event_loop()
        drone = loop.run_until_complete(connect_drone())
        status = loop.run_until_complete(pause_mission(drone))
        return JsonResponse(status)>>
def resume_mission_view(request):
    if request.method == 'POST':
        loop = asyncio.get_event_loop()
        drone = loop.run_until_complete(connect_drone())
        status = loop.run_until_complete(resume_mission(drone))
        return JsonResponse(status)

@csrf_exempt
def return_to_base_view(request):
    if request.method == 'POST':
        loop = asyncio.get_event_loop()
        drone = loop.run_until_complete(connect_drone())
        status = loop.run_until_complete(return_to_base(drone))
        return JsonResponse(status)" >> DjangoFBL/views.py 

echo "from django.urls import path
from . import views

urlpatterns = [
    path('connect_to_drone/', views.connect_to_drone, name='connect_to_drone'),
    path('get_live_coordinates/', views.get_live_coordinates, name='get_live_coordinates'),
    path('start_mission/', views.start_mission, name='start_mission'),
    path('pause_mission/', views.pause_mission, name='pause_mission'),
    path('resume_mission/', views.resume_mission, name='resume_mission'),
    path('return_to_base/', views.return_to_base, name='return_to_base'),
    path('get_mission/', views.get_mission, name='get_mission')," >> DjangoFBL/urls.py

cd .. 



