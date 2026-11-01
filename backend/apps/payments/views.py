from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payments.models import Payment


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        method = request.data.get("method", "wallet")
        amount = request.data.get("amount", 0)
        emergency_id = request.data.get("emergency_id")

        payment = Payment.objects.create(
            tenant=request.user.tenant,
            user=request.user,
            emergency_id=emergency_id,
            amount=amount,
            method=method,
            status=Payment.Status.PENDING,
        )

        if method == "razorpay":
            payment.gateway_ref = f"rzp_{payment.id}"
        elif method == "stripe":
            payment.gateway_ref = f"stripe_{payment.id}"
        elif method == "wallet":
            if request.user.emergency_wallet_balance >= amount:
                request.user.emergency_wallet_balance -= amount
                request.user.save(update_fields=["emergency_wallet_balance"])
                payment.status = Payment.Status.COMPLETED
            else:
                return Response({"detail": "Insufficient wallet balance"}, status=400)
        elif method == "cash":
            payment.status = Payment.Status.COMPLETED

        payment.save()
        return Response({"id": str(payment.id), "status": payment.status}, status=status.HTTP_201_CREATED)
