from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def broadcast_emergency_update(emergency_id: str, payload: dict):
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            f"emergency_{emergency_id}",
            {"type": "emergency.message", "payload": payload},
        )
