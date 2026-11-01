from django.urls import path

from apps.accounts.admin_panel_views import (
    AdminAnalyticsView,
    AdminBackupView,
    AdminEmergenciesView,
    AdminSystemHealthView,
)

urlpatterns = [
    path("analytics/", AdminAnalyticsView.as_view()),
    path("emergencies/live/", AdminEmergenciesView.as_view()),
    path("system/health/", AdminSystemHealthView.as_view()),
    path("backup/trigger/", AdminBackupView.as_view()),
]
