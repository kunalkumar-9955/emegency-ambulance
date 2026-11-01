import pytest
from django.contrib.auth import get_user_model
from apps.accounts.models import UserRole
from apps.core.models import Tenant

User = get_user_model()


@pytest.mark.django_db
def test_user_registration_role_restriction():
    tenant = Tenant.objects.create(name="Test", slug="test-tenant")
    user = User.objects.create_user(
        username="patient@test.com",
        email="patient@test.com",
        password="testpass123",
        role=UserRole.PATIENT,
        tenant=tenant,
    )
    assert user.role == UserRole.PATIENT
