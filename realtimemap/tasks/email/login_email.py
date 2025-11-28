from datetime import datetime
from typing import Optional

from core.celery import app
from .common import render_html, send_email


@app.task
def login_email(
    recipient: str,
    username: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    timestamp: Optional[datetime] = None,
):
    if timestamp is None:
        timestamp = datetime.now()

    html = render_html(
        "login_notification.html",
        context={
            "username": username,
            "ip_address": ip_address or "Unknown",
            "timestamp": timestamp,
            "user_agent": user_agent or "Unknown",
        },
    )
    send_email(
        recipients=[recipient],
        subject="Login Notification",
        html_content=html,
    )
