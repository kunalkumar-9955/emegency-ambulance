from django.urls import path
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.notifications.models import Notification


class NotificationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()[:50]
        return Response([
            {"id": str(n.id), "title": n.title, "body": n.body, "is_read": n.is_read, "sent_at": n.sent_at}
            for n in qs
        ])

urlpatterns = [
    path("notifications/", NotificationListView.as_view()),
]
