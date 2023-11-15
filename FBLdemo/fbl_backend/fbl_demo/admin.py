from django.contrib import admin
from .models import Drone

class DroneAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('name', 'model_type', 'status', 'last_updated')

    # Adding filter options for better sorting and viewing
    list_filter = ('status', 'model_type')

    # Adding search functionality to find drones by name and model type
    search_fields = ('name', 'model_type')

    # Customizing the form view in the admin
    # This allows for editing specific fields when you click into a drone record
    fields = ('name', 'model_type', 'status')

    # Custom action to quickly change the status of selected drones
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(status='active')
    make_active.short_description = "Mark selected drones as active"

    def make_inactive(self, request, queryset):
        queryset.update(status='inactive')
    make_inactive.short_description = "Mark selected drones as inactive"

# Register your models here
admin.site.register(Drone, DroneAdmin)

