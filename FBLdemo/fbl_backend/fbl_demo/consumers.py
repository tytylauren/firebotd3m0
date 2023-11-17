# fbl_demo/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DroneStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'drone_operations'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'status_update':
            await self.handle_status_update(data)
        elif message_type == 'launch_command':
            await self.handle_launch_command(data)
        # Add more message types as needed

    async def handle_status_update(self, data):
        # Process drone status update
        drone_id = data['drone_id']
        status = data['status']

        # Broadcast status update
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'broadcast_message',
                'message': f'Drone {drone_id} status: {status}'
            }
        )

    async def handle_launch_command(self, data):
        # Process launch command for a drone
        drone_id = data['drone_id']
        # Add logic for handling drone launch

        # Broadcast launch confirmation
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'broadcast_message',
                'message': f'Drone {drone_id} launch initiated'
            }
        )

    # Receive message from room group
    async def broadcast_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

