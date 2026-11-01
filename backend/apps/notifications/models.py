import uuid

from django.conf import settings
from django.db import models


class Notification(models.Model):
    class Channel(models.TextChoices):
        PUSH = "push", "Push"
        SMS = "sms", "SMS"
        EMAIL = "email", "Email"
        VOICE = "voice", "Voice Alert"
        IN_APP = "in_app", "In App"

    class Priority(models.TextChoices):
        NORMAL = "normal", "Normal"
        HIGH = "high", "High"
        EMERGENCY = "emergency", "Emergency"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    body = models.TextField()
    channel = models.CharField(max_length=20, choices=Channel.choices, default=Channel.IN_APP)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.NORMAL)
    data = models.JSONField(default=dict, blank=True)
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-sent_at"]
