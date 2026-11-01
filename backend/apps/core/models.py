import uuid

from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tenant(TimeStampedModel):
    """Multi-tenant organization (hospital network / city operator)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    settings = models.JSONField(default=dict, blank=True)
    subscription_plan = models.CharField(max_length=50, default="basic")
    max_ambulances = models.PositiveIntegerField(default=50)

    class Meta:
        db_table = "tenants"

    def __str__(self):
        return self.name


class TenantScopedModel(TimeStampedModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="%(class)ss")

    class Meta:
        abstract = True
