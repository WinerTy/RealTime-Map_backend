from celery import Celery

from core.config import conf

app = Celery(
    "core.celery.celery_app",
    broker=str(conf.redis.url),
    backend=str(conf.redis.url),
    include=["tasks"],
)

app.conf.beat_schedule = {}
