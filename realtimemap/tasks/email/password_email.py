from typing import Optional

from core.celery import app
from .common import render_html, send_email


@app.task
def forgot_password_email(recipient: str, username: str, reset_url: str):
    html = render_html(
        "password_reset.html",
        context={
            "username": username,
            "reset_url": reset_url,
        },
    )
    send_email(
        recipients=[recipient],
        subject="Password Reset Request",
        html_content=html,
    )


@app.task
def change_password_email(
    recipient: str, username: str, ip_address: Optional[str] = None
):
    html = render_html(
        "password_changed.html",
        context={
            "username": username,
            "ip_address": ip_address or "Unknown",
        },
    )
    send_email(
        recipients=[recipient],
        subject="Password Change",
        html_content=html,
    )
