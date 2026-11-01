from apps.audit.models import AuditLog


def log_audit(user, action, resource_type, resource_id="", details=None, request=None):
    meta = getattr(request, "audit_meta", {}) if request else {}
    AuditLog.objects.create(
        user=user,
        action=action,
        resource_type=resource_type,
        resource_id=str(resource_id),
        ip_address=meta.get("ip"),
        user_agent=meta.get("user_agent", ""),
        details=details or {},
    )
