from django.urls import re_path

from apps.realtime.consumers import DriverTrackingConsumer, EmergencyConsumer

websocket_urlpatterns = [
    re_path(r"ws/emergency/(?P<emergency_id>[0-9a-f-]+)/$", EmergencyConsumer.as_asgi()),
    re_path(r"ws/driver/(?P<driver_id>[0-9a-f-]+)/$", DriverTrackingConsumer.as_asgi()),
]
