from rest_framework import serializers
from .models import Drone

class DroneSerializer(serializers.ModelSerializer):
    # Additional fields for detailed drone information
    battery_level = serializers.IntegerField(min_value=0, max_value=100, required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    altitude = serializers.FloatField(required=False)

    def validate(self, data):
        if data['status'] == 'flying' and ('latitude' not in data or 'longitude' not in data):
            raise serializers.ValidationError("Flying drones must have latitude and longitude.")

        if data['status'] == 'inactive' and 'battery_level' in data and data['battery_level'] < 20:
            raise serializers.ValidationError("Inactive drones should not have a battery level below 20%.")

        return data

    class Meta:
        model = Drone
        fields = '__all__'
        # Optionally, specify read-only fields
        # read_only_fields = ('id', 'last_updated',)

    # Custom method to handle specific logic
    def update_drone_status(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.altitude = validated_data.get('altitude', instance.altitude)
        instance.battery_level = validated_data.get('battery_level', instance.battery_level)
        instance.save()
        return instance

    # Override the create or update methods if needed
    # def create(self, validated_data):
    #     # Custom creation logic
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     # Custom update logic
    #     return super().update(instance, validated_data)

