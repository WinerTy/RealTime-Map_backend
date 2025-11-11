from datetime import datetime

from sqlalchemy import select

from core.celery import app
from database.helper import db_helper
from modules import Mark


@app.task
def check_mark_ended():
    count_updated = 0
    with db_helper.sync_session_factory() as session:
        stmt = select(Mark).where(
            Mark.is_ended.is_(False),
        )  # Md add same logic here
        result = session.execute(stmt).scalars().all()
        for mark in result:
            if mark.end_at <= datetime.now():
                count_updated += 1
                mark.is_ended = True

        session.commit()
    return count_updated
