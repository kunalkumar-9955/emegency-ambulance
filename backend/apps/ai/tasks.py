from celery import shared_task

from apps.ai.services.analytics import generate_daily_analytics


@shared_task(queue="ai")
def run_daily_analytics():
    generate_daily_analytics()
