import uuid

from django.conf import settings
from django.db import models

from apps.core.models import TenantScopedModel


class Hospital(TenantScopedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    phone = models.CharField(max_length=20)
    icu_beds_total = models.PositiveIntegerField(default=0)
    icu_beds_available = models.PositiveIntegerField(default=0)
    general_beds_available = models.PositiveIntegerField(default=0)
    has_trauma_center = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    specialties = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = "hospitals"

    def __str__(self):
        return self.name


class Ambulance(TenantScopedModel):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        BUSY = "busy", "Busy"
        MAINTENANCE = "maintenance", "Maintenance"
        OFFLINE = "offline", "Offline"

    class AmbulanceType(models.TextChoices):
        BASIC = "basic", "Basic Life Support"
        ADVANCED = "advanced", "Advanced Life Support"
        ICU = "icu", "ICU Ambulance"
        NEONATAL = "neonatal", "Neonatal"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle_number = models.CharField(max_length=50)
    ambulance_type = models.CharField(max_length=20, choices=AmbulanceType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OFFLINE)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    equipment = models.JSONField(default=list, blank=True)
    supports_drone_link = models.BooleanField(default=False)

    class Meta:
        db_table = "ambulances"

    def __str__(self):
        return self.vehicle_number


class Driver(TenantScopedModel):
    class Availability(models.TextChoices):
        ONLINE = "online", "Online"
        OFFLINE = "offline", "Offline"
        ON_TRIP = "on_trip", "On Trip"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="driver_profile")
    license_number = models.CharField(max_length=50)
    ambulance = models.ForeignKey(Ambulance, on_delete=models.SET_NULL, null=True, blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    availability = models.CharField(max_length=20, choices=Availability.choices, default=Availability.OFFLINE)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    total_trips = models.PositiveIntegerField(default=0)
    earnings_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_service_date = models.DateField(null=True, blank=True)
    fuel_reminder_km = models.PositiveIntegerField(default=5000)

    class Meta:
        db_table = "drivers"

    def __str__(self):
        return str(self.user.email)
