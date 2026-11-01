import uuid

from django.db import models

from apps.core.models import Tenant


class AIAnalytics(models.Model):
    class ReportType(models.TextChoices):
        HOTSPOT = "hotspot", "Emergency Hotspot"
        PEAK_TIME = "peak_time", "Peak Emergency Time"
        DRIVER_PERF = "driver_perf", "Driver Performance"
        HOSPITAL_LOAD = "hospital_load", "Hospital Load"
        RESPONSE_TIME = "response_time", "Response Time"
        PREDICTION = "prediction", "Emergency Prediction"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)
    report_type = models.CharField(max_length=30, choices=ReportType.choices)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    data = models.JSONField(default=dict)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ai_analytics"
        verbose_name_plural = "AI Analytics"


class DroneDispatch(models.Model):
    """Future-ready drone ambulance support."""

    class MissionType(models.TextChoices):
        BLOOD = "blood", "Blood Delivery"
        MEDICINE = "medicine", "Medicine Delivery"
        AED = "aed", "AED Delivery"

    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        IN_FLIGHT = "in_flight", "In Flight"
        DELIVERED = "delivered", "Delivered"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emergency_id = models.UUIDField()
    mission_type = models.CharField(max_length=20, choices=MissionType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED)
    destination_lat = models.DecimalField(max_digits=9, decimal_places=6)
    destination_lng = models.DecimalField(max_digits=9, decimal_places=6)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "drone_dispatches"
