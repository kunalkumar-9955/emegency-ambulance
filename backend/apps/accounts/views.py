from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.models import DeviceSession
from apps.accounts.permissions import IsSuperAdmin
from apps.accounts.serializers import (
    CustomTokenObtainPairSerializer,
    DeviceSessionSerializer,
    EmergencyContactSerializer,
    RegisterSerializer,
    UserSerializer,
)
from apps.audit.models import AuditLog
from apps.audit.services import log_audit
from apps.emergencies.models import EmergencyContact

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(email=request.data.get("email"))
            log_audit(user, AuditLog.Action.LOGIN, "auth", details={"method": "jwt"}, request=request)
        return response


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class DeviceSessionView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSessionSerializer

    def get_queryset(self):
        return DeviceSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        meta = getattr(self.request, "audit_meta", {})
        DeviceSession.objects.update_or_create(
            user=self.request.user,
            device_id=serializer.validated_data["device_id"],
            defaults={
                **serializer.validated_data,
                "ip_address": meta.get("ip"),
                "is_active": True,
            },
        )


class EmergencyContactListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmergencyContactSerializer

    def get_queryset(self):
        return EmergencyContact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        log_audit(request.user, AuditLog.Action.LOGOUT, "auth", request=request)
        return Response({"detail": "Logged out. Blacklist refresh token on client."})


class UserManagementView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by("-date_joined")
