from django.test import TestCase
from django.urls import reverse
from .models import Drone
from rest_framework import status
from rest_framework.test import APIClient
import json

class DroneModelTests(TestCase):
    def setUp(self):
        # Create test drones with different statuses
        Drone.objects.create(name="TestDrone1", model_type="TypeA", status="inactive")
        Drone.objects.create(name="TestDrone2", model_type="TypeB", status="active")
        Drone.objects.create(name="TestDrone3", model_type="TypeC", status="charging")

    def test_drone_status(self):
        """Test the drone model's status field."""
        drone1 = Drone.objects.get(name="TestDrone1")
        drone2 = Drone.objects.get(name="TestDrone2")
        drone3 = Drone.objects.get(name="TestDrone3")
        self.assertEqual(drone1.status, "inactive")
        self.assertEqual(drone2.status, "active")
        self.assertEqual(drone3.status, "charging")

    def test_drone_str_method(self):
        """Test the string representation of the Drone model."""
        drone = Drone.objects.get(name="TestDrone1")
        self.assertEqual(str(drone), "TestDrone1")

class DroneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.drone1 = Drone.objects.create(name="TestDrone1", model_type="TypeA", status="inactive")
        self.drone2 = Drone.objects.create(name="TestDrone2", model_type="TypeB", status="active")

    def test_get_drones(self):
        """Test retrieving a list of drones."""
        response = self.client.get(reverse('drone-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_update_drone_status(self):
        """Test updating a drone's status."""
        response = self.client.patch(
            reverse('drone-detail', kwargs={'pk': self.drone1.pk}),
            data=json.dumps({'status': 'active'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.drone1.refresh_from_db()
        self.assertEqual(self.drone1.status, 'active')

    def test_launch_simulation(self):
        """Test the launch simulation view."""
        response = self.client.post(reverse('launch_simulation'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Simulation started", response.content.decode())

    # Additional tests for other functionalities and edge cases

