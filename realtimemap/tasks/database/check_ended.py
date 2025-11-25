import logging
from contextlib import contextmanager

from sqlalchemy import update, text

from core.celery import app
from database import get_sync_session
from modules import Mark

session_context = contextmanager(get_sync_session)

logger = logging.getLogger(__name__)


@app.task
def check_mark_ended():
    """
    Проверяет и помечает истекшие метки.

    Использует массовое обновление (bulk update) вместо цикла для максимальной производительности.
    Вычисление end_at происходит на уровне БД через SQL выражение (start_at + duration часов).

    Преимущества перед старым подходом:
    - Один SQL запрос вместо N+1
    - Не загружает данные в память Python
    - Вычисление времени на стороне БД
    - В 10-100 раз быстрее при больших объемах

    Returns:
        int: Количество обновленных меток
    """
    with session_context() as session:
        logger.info("Start check_mark_ended")

        # Массовое обновление одним запросом
        stmt = (
            update(Mark)
            .where(
                Mark.is_ended.is_(False),
                text("start_at + (duration * interval '1 hour') <= NOW()"),
            )
            .values(is_ended=True)
            .execution_options(synchronize_session=False)
        )

        result = session.execute(stmt)
        count_updated = result.rowcount
        session.commit()

        if count_updated > 0:
            logger.info(f"Marked as ended: {count_updated} marks")
        else:
            logger.info("No expired marks found")

        return count_updated
