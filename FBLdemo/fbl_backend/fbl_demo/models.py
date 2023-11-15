from django.db import models
from django.core.exceptions import ValidationError

class Drone(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('flying', 'Flying'),
        ('on_mission', 'On Mission'),  # When the drone is executing a specific task
        ('charging', 'Charging'),  # When the drone is recharging its battery
        ('maintenance', 'Maintenance'),  # When the drone is undergoing maintenance
        ('error', 'Error'),  # When the drone encounters an error or malfunction
        ('standby', 'Standby'),  # When the drone is ready but not currently active
        ('returning', 'Returning'),  # When the drone is returning to base
        ('deploying', 'Deploying'),  # When the drone is in the process of being deployed
        # Add more statuses as needed
    ]

    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='inactive')
    last_updated = models.DateTimeField(auto_now=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    battery_level = models.IntegerField(null=True, blank=True)  # Assuming percentage

    def __str__(self):
        return self.name

    def clean(self):
        # Add any custom validation here
        super().clean()

