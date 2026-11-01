import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models import Tenant


class UserRole(models.TextChoices):
    PATIENT = "patient", "Patient"
    DRIVER = "driver", "Driver"
    HOSPITAL_ADMIN = "hospital_admin", "Hospital Admin"
    SUPER_ADMIN = "super_admin", "Super Admin"
    VOLUNTEER = "volunteer", "Volunteer"


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.PATIENT)
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True)
    language = models.CharField(max_length=10, default="en")
    is_verified = models.BooleanField(default=False)
    medical_profile = models.JSONField(default=dict, blank=True)
    e2e_public_key = models.TextField(blank=True, help_text="Base64 NaCl public key")
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    emergency_wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"
        indexes = [models.Index(fields=["role", "tenant"])]

    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def is_super_admin(self):
        return self.role == UserRole.SUPER_ADMIN

    @property
    def is_driver(self):
        return self.role == UserRole.DRIVER

    @property
    def is_hospital_admin(self):
        return self.role == UserRole.HOSPITAL_ADMIN


class DeviceSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="device_sessions")
    device_id = models.CharField(max_length=255)
    device_name = models.CharField(max_length=255, blank=True)
    platform = models.CharField(max_length=50)  # android, ios, web
    app_version = models.CharField(max_length=20, blank=True)
    fcm_token = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "device_sessions"
        unique_together = [["user", "device_id"]]
