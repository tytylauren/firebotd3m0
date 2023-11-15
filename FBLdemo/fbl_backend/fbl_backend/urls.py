# fbl_backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fbl_demo.urls')),  # Includes URLs from the fbl_demo app
]

