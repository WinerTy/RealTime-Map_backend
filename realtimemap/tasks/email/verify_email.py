from core.celery import app
from core.config import conf
from .common import render_html, send_email


@app.task
def verify_email(recipient: str, username: str, token: str):
    html = render_html(
        "verify_email.html",
        context={"token": token, "username": username, "base_url": conf.frontend.url},
    )
    send_email(
        recipients=[recipient],
        subject="Verify Email",
        html_content=html,
    )
