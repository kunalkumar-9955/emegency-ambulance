import uuid

from django.conf import settings
from django.db import models

from apps.core.models import TenantScopedModel
from apps.emergencies.models import EmergencyRequest


class Payment(TenantScopedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    class Method(models.TextChoices):
        UPI = "upi", "UPI"
        RAZORPAY = "razorpay", "Razorpay"
        STRIPE = "stripe", "Stripe"
        WALLET = "wallet", "Wallet"
        CASH = "cash", "Cash"
        SUBSCRIPTION = "subscription", "Subscription"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    emergency = models.ForeignKey(EmergencyRequest, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="INR")
    method = models.CharField(max_length=20, choices=Method.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    gateway_ref = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "payments"
