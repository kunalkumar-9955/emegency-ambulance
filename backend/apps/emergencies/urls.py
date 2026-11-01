from django.urls import path

from apps.emergencies.views import (
    DriverAcceptView,
    EmergencyDetailView,
    EmergencyListView,
    GPSPingView,
    OfflineSyncView,
    SOSView,
)

urlpatterns = [
    path("emergencies/sos/", SOSView.as_view(), name="sos"),
    path("emergencies/", EmergencyListView.as_view(), name="emergency-list"),
    path("emergencies/<uuid:id>/", EmergencyDetailView.as_view(), name="emergency-detail"),
    path("emergencies/<uuid:id>/accept/", DriverAcceptView.as_view(), name="emergency-accept"),
    path("emergencies/<uuid:id>/gps/", GPSPingView.as_view(), name="emergency-gps"),
    path("emergencies/offline-sync/", OfflineSyncView.as_view(), name="offline-sync"),
]
