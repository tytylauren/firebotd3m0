# fbl_demo/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/drone_status/$', consumers.DroneStatusConsumer.as_asgi()),
]

