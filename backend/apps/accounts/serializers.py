from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.models import DeviceSession, UserRole
from apps.emergencies.models import EmergencyContact

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "email", "phone", "role", "language", "is_verified",
            "medical_profile", "e2e_public_key", "emergency_wallet_balance",
            "first_name", "last_name", "avatar",
        ]
        read_only_fields = ["id", "role", "is_verified", "emergency_wallet_balance"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "password", "phone", "first_name", "last_name", "role", "language"]

    def validate_role(self, value):
        if value in (UserRole.SUPER_ADMIN, UserRole.HOSPITAL_ADMIN):
            raise serializers.ValidationError("Cannot self-register as admin.")
        return value or UserRole.PATIENT

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.username = validated_data["email"]
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["tenant_id"] = str(user.tenant_id) if user.tenant_id else None
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data


class DeviceSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceSession
        fields = ["id", "device_id", "device_name", "platform", "app_version", "fcm_token", "is_active", "last_seen"]
        read_only_fields = ["id", "last_seen"]


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ["id", "name", "phone", "relationship", "notify_on_emergency", "can_track_live"]
        read_only_fields = ["id"]
