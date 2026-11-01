import uuid

from django.db import models


class OTAUpdate(models.Model):
    class Platform(models.TextChoices):
        ANDROID = "android", "Android"
        IOS = "ios", "iOS"
        ALL = "all", "All Platforms"

    class UpdateType(models.TextChoices):
        OPTIONAL = "optional", "Optional"
        RECOMMENDED = "recommended", "Recommended"
        CRITICAL = "critical", "Critical (Force)"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    app_name = models.CharField(max_length=50)  # patient, driver
    version = models.CharField(max_length=20)
    build_number = models.PositiveIntegerField()
    platform = models.CharField(max_length=10, choices=Platform.choices)
    update_type = models.CharField(max_length=20, choices=UpdateType.choices)
    download_url = models.URLField()
    changelog = models.TextField()
    min_supported_version = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    is_rolled_back = models.BooleanField(default=False)
    rolled_back_from = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    pushed_at = models.DateTimeField(auto_now_add=True)
    pushed_by = models.UUIDField(null=True, blank=True)

    class Meta:
        db_table = "ota_updates"
        ordering = ["-build_number"]
        unique_together = [["app_name", "version", "platform"]]
