import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("emergency_ambulance")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.task_routes = {
    "apps.emergencies.tasks.*": {"queue": "emergency"},
    "apps.ai.tasks.*": {"queue": "ai"},
    "apps.notifications.tasks.*": {"queue": "notifications"},
}
