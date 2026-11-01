from celery import shared_task


@shared_task(queue="notifications")
def send_push_notification(user_id: str, title: str, body: str, data=None):
    from apps.accounts.models import DeviceSession
    from apps.notifications.models import Notification

    Notification.objects.create(
        user_id=user_id,
        title=title,
        body=body,
        channel="push",
        priority="emergency" if "EMERGENCY" in title.upper() else "normal",
        data=data or {},
    )
    sessions = DeviceSession.objects.filter(user_id=user_id, is_active=True).exclude(fcm_token="")
    for session in sessions:
        _send_fcm(session.fcm_token, title, body)


def _send_fcm(token, title, body):
    # Integrate Firebase Admin SDK with settings.FCM_SERVER_KEY
    pass


@shared_task(queue="notifications")
def send_sms(phone: str, message: str):
    from django.conf import settings
    if not settings.TWILIO_ACCOUNT_SID:
        return
    try:
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(body=message[:160], from_=settings.TWILIO_FROM_NUMBER, to=phone)
    except Exception:
        pass
