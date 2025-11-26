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
    # Переодическая задача для проверки меток
    "end_check": {
        "task": "tasks.database.check_ended.check_mark_ended",
        "schedule": crontab(minute=30),
    },
    # Полная синхронизация пользователей и их статистики
    "sync_all_metrics": {
        "task": "tasks.database.sync_metrics.sync_user_metrics",
        "schedule": crontab(hour=12),
    },
    # Синхронизация только активных пользователей за 24 часа
    "sync_active_metrics": {
        "task": "tasks.database.sync_metrics.sync_active_user_metrics",
        "schedule": crontab(minute=15),
    },
}
