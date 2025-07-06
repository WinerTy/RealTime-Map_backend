from celery import Celery
from celery.schedules import crontab

from core.config import conf

app = Celery(
    "core.celery.celery_app",
    broker=conf.celery.broker,
    backend=conf.celery.backend,
    include=["tasks"],
)

app.conf.beat_schedule = {
    "end_check": {
        "task": "tasks.database.check_ended.check_mark_ended",  # Md Rename
        "schedule": crontab(minute=15),
    }
}
