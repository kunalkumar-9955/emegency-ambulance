import uuid

from django.conf import settings
from django.db import models

from apps.core.models import TenantScopedModel
from apps.fleet.models import Ambulance, Driver, Hospital


class EmergencyRequest(TenantScopedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        DISPATCHING = "dispatching", "Dispatching"
        ASSIGNED = "assigned", "Assigned"
        EN_ROUTE = "en_route", "En Route"
        ARRIVED = "arrived", "Arrived"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    class Source(models.TextChoices):
        APP = "app", "Mobile App"
        WEB = "web", "Website"
        SMS = "sms", "SMS Offline"
        VOICE = "voice", "Voice Assistant"
        WEARABLE = "wearable", "Wearable Device"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="emergencies")
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    ambulance = models.ForeignKey(Ambulance, on_delete=models.SET_NULL, null=True, blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.HIGH)
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.APP)
    is_sos = models.BooleanField(default=False)
    symptoms = models.TextField(blank=True)
    emergency_type = models.CharField(max_length=100, blank=True)
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_address = models.TextField(blank=True)
    destination_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    destination_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    eta_minutes = models.PositiveIntegerField(null=True, blank=True)
    ai_severity_score = models.FloatField(null=True, blank=True)
    ai_fraud_score = models.FloatField(null=True, blank=True)
    fraud_flagged = models.BooleanField(default=False)
    voice_stress_score = models.FloatField(null=True, blank=True)
    wearable_data = models.JSONField(default=dict, blank=True)
    medical_reports = models.JSONField(default=list, blank=True)
    encrypted_notes = models.TextField(blank=True)
    offline_sync_id = models.CharField(max_length=100, blank=True, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "emergency_requests"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "priority"]),
            models.Index(fields=["patient", "-created_at"]),
        ]


class EmergencyContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="emergency_contacts")
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    relationship = models.CharField(max_length=50, blank=True)
    notify_on_emergency = models.BooleanField(default=True)
    can_track_live = models.BooleanField(default=True)

    class Meta:
        db_table = "emergency_contacts"


class GPSLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emergency = models.ForeignKey(EmergencyRequest, on_delete=models.CASCADE, related_name="gps_logs", null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    ambulance = models.ForeignKey(Ambulance, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    speed_kmh = models.FloatField(null=True, blank=True)
    heading = models.FloatField(null=True, blank=True)
    accuracy_meters = models.FloatField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "gps_logs"
        ordering = ["-recorded_at"]


class CrowdAlert(TenantScopedModel):
    """Emergency crowd volunteer notification."""

    class AlertType(models.TextChoices):
        CPR = "cpr", "CPR Needed"
        BLOOD = "blood", "Blood Required"
        GENERAL = "general", "General Assistance"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emergency = models.ForeignKey(EmergencyRequest, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=AlertType.choices)
    radius_km = models.FloatField(default=2.0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    volunteers_notified = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "crowd_alerts"
