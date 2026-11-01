from rest_framework import serializers

from apps.fleet.models import Ambulance, Driver, Hospital


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"
        read_only_fields = ["id", "tenant", "created_at", "updated_at"]


class AmbulanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambulance
        fields = "__all__"
        read_only_fields = ["id", "tenant", "created_at", "updated_at"]


class DriverSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Driver
        fields = [
            "id", "email", "license_number", "ambulance", "hospital",
            "availability", "rating", "total_trips", "earnings_total",
            "latitude", "longitude",
        ]
        read_only_fields = ["id", "rating", "total_trips", "earnings_total"]
