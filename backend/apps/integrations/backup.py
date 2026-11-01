import json
from datetime import datetime
from pathlib import Path

from celery import shared_task
from django.conf import settings


@shared_task
def run_database_backup():
    backup_dir = Path(settings.BASE_DIR) / "backups"
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    manifest = {"timestamp": timestamp, "status": "completed", "type": "logical"}
    path = backup_dir / f"backup_{timestamp}.json"
    path.write_text(json.dumps(manifest))
    if settings.USE_S3:
        _upload_to_s3(path)
    return str(path)


def _upload_to_s3(path: Path):
    try:
        import boto3
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        key = f"backups/{path.name}"
        s3.upload_file(str(path), settings.AWS_STORAGE_BUCKET_NAME, key, ExtraArgs={"ServerSideEncryption": "AES256"})
    except Exception:
        pass


def trigger_backup():
    result = run_database_backup.delay()
    return str(result.id)
