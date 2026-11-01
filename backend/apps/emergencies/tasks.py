from celery import shared_task
from django.utils import timezone

from apps.emergencies.models import EmergencyRequest
from apps.notifications.tasks import send_push_notification
from apps.realtime.broadcast import broadcast_emergency_update


@shared_task(queue="emergency")
def dispatch_emergency(emergency_id: str):
    from apps.ai.services.dispatch import run_smart_dispatch

    emergency = EmergencyRequest.objects.get(id=emergency_id)
    emergency.status = EmergencyRequest.Status.DISPATCHING
    emergency.save(update_fields=["status"])

    result = run_smart_dispatch(emergency)
    if result.get("driver_id"):
        from apps.fleet.models import Driver

        driver = Driver.objects.get(id=result["driver_id"])
        emergency.driver = driver
        emergency.ambulance = driver.ambulance
        emergency.eta_minutes = result.get("eta_minutes")
        if result.get("hospital_id"):
            from apps.fleet.models import Hospital
            emergency.hospital = Hospital.objects.get(id=result["hospital_id"])
        emergency.status = EmergencyRequest.Status.ASSIGNED
        emergency.save()
        driver.availability = "on_trip"
        driver.save(update_fields=["availability"])
        send_push_notification.delay(str(driver.user_id), "New Emergency", "Emergency request assigned")
        broadcast_emergency_update(emergency_id, {"event": "assigned", "eta": emergency.eta_minutes})


@shared_task(queue="notifications")
def notify_emergency_contacts(emergency_id: str):
    from apps.emergencies.models import EmergencyContact

    emergency = EmergencyRequest.objects.select_related("patient").get(id=emergency_id)
    contacts = EmergencyContact.objects.filter(user=emergency.patient, notify_on_emergency=True)
    for contact in contacts:
        from apps.notifications.tasks import send_sms

        send_sms.delay(contact.phone, f"EMERGENCY: {emergency.patient.get_full_name()} triggered SOS.")


@shared_task
def complete_emergency(emergency_id: str):
    EmergencyRequest.objects.filter(id=emergency_id).update(
        status=EmergencyRequest.Status.COMPLETED,
        completed_at=timezone.now(),
    )
