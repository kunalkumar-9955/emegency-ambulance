from django.urls import path

from apps.fleet.views import DriverAvailabilityView, FleetManagementView, HospitalListView

urlpatterns = [
    path("hospitals/", HospitalListView.as_view()),
    path("drivers/availability/", DriverAvailabilityView.as_view()),
    path("fleet/ambulances/", FleetManagementView.as_view()),
]
