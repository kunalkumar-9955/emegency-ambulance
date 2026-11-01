from django.urls import path

from apps.ota.views import OTACheckView, OTAPushView, OTARollbackView

urlpatterns = [
    path("ota/check/", OTACheckView.as_view()),
    path("ota/push/", OTAPushView.as_view()),
    path("ota/<uuid:id>/rollback/", OTARollbackView.as_view()),
]
