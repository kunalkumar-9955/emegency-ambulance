import json

from channels.generic.websocket import AsyncWebsocketConsumer


class EmergencyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.emergency_id = self.scope["url_route"]["kwargs"]["emergency_id"]
        self.group_name = f"emergency_{self.emergency_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "emergency.message", "payload": data},
        )

    async def emergency_message(self, event):
        await self.send(text_data=json.dumps(event["payload"]))


class DriverTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.driver_id = self.scope["url_route"]["kwargs"]["driver_id"]
        self.group_name = f"driver_{self.driver_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def driver_message(self, event):
        await self.send(text_data=json.dumps(event["payload"]))
