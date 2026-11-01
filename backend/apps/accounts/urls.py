from django.urls import path

from apps.accounts.views import (
    DeviceSessionView,
    EmergencyContactListView,
    LogoutView,
    ProfileView,
    RegisterView,
    UserManagementView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("users/me/", ProfileView.as_view(), name="profile"),
    path("devices/", DeviceSessionView.as_view(), name="devices"),
    path("emergency-contacts/", EmergencyContactListView.as_view(), name="emergency-contacts"),
    path("admin/users/", UserManagementView.as_view(), name="admin-users"),
]
