from django.urls import path

from apps.payments.views import CreatePaymentView

urlpatterns = [
    path("payments/create/", CreatePaymentView.as_view()),
]
