from django.core.management.base import BaseCommand

from apps.accounts.models import User, UserRole
from apps.core.models import Tenant


class Command(BaseCommand):
    help = "Seed default tenant and roles"

    def handle(self, *args, **options):
        tenant, _ = Tenant.objects.get_or_create(
            slug="default",
            defaults={"name": "Default Emergency Network", "subscription_plan": "enterprise"},
        )
        if not User.objects.filter(email="admin@emergency.local").exists():
            admin = User.objects.create_superuser(
                username="admin",
                email="admin@emergency.local",
                password="Admin@123ChangeMe",
                role=UserRole.SUPER_ADMIN,
                tenant=tenant,
            )
            self.stdout.write(self.style.SUCCESS(f"Super admin created: {admin.email}"))
        self.stdout.write(self.style.SUCCESS("Seed complete"))
