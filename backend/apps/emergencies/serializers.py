from rest_framework import serializers

from apps.emergencies.models import EmergencyContact, EmergencyRequest, GPSLog


class EmergencyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyRequest
        fields = [
            "id", "status", "priority", "source", "is_sos", "symptoms", "emergency_type",
            "pickup_latitude", "pickup_longitude", "pickup_address",
            "destination_latitude", "destination_longitude",
            "eta_minutes", "ai_severity_score", "fraud_flagged",
            "driver", "ambulance", "hospital", "medical_reports", "wearable_data",
            "created_at", "updated_at", "completed_at",
        ]
        read_only_fields = [
            "id", "status", "eta_minutes", "ai_severity_score", "fraud_flagged",
            "driver", "ambulance", "hospital", "created_at", "updated_at", "completed_at",
        ]


class SOSSerializer(serializers.Serializer):
    pickup_latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    pickup_longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    pickup_address = serializers.CharField(required=False, allow_blank=True)
    symptoms = serializers.CharField(required=False, allow_blank=True)
    emergency_type = serializers.CharField(required=False, allow_blank=True)
    wearable_data = serializers.JSONField(required=False)
    voice_stress_score = serializers.FloatField(required=False)
    offline_sync_id = serializers.CharField(required=False, allow_blank=True)


class GPSLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSLog
        fields = ["latitude", "longitude", "speed_kmh", "heading", "accuracy_meters", "recorded_at"]
