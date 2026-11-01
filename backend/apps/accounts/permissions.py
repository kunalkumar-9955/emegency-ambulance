from rest_framework.permissions import BasePermission

from apps.accounts.models import UserRole


class IsRole(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )


class IsPatient(IsRole):
    allowed_roles = [UserRole.PATIENT]


class IsDriver(IsRole):
    allowed_roles = [UserRole.DRIVER]


class IsHospitalAdmin(IsRole):
    allowed_roles = [UserRole.HOSPITAL_ADMIN]


class IsSuperAdmin(IsRole):
    allowed_roles = [UserRole.SUPER_ADMIN]


class IsHospitalOrSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.role in (UserRole.HOSPITAL_ADMIN, UserRole.SUPER_ADMIN)
        )


class IsAdminPanelRequest(BasePermission):
    """Localhost super admin panel — requires secret header."""

    def has_permission(self, request, view):
        from django.conf import settings

        host = request.META.get("HTTP_HOST", "").split(":")[0]
        if host not in settings.ADMIN_PANEL_ALLOWED_HOSTS:
            return False
        secret = request.META.get("HTTP_X_ADMIN_PANEL_KEY", "")
        return (
            secret == settings.ADMIN_PANEL_SECRET
            and request.user.is_authenticated
            and request.user.role == UserRole.SUPER_ADMIN
        )
