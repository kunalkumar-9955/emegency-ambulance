class AuditMiddleware:
    """Attach request metadata for audit logging."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.audit_meta = {
            "ip": self._get_client_ip(request),
            "user_agent": request.META.get("HTTP_USER_AGENT", "")[:500],
        }
        return self.get_response(request)

    @staticmethod
    def _get_client_ip(request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
