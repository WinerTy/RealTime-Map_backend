from core.celery import app
from .common import render_html, send_email


@app.task
def verify_email(recipient: str, username: str, verify_url: str):
    """
    Задача по отправке письма при верификации письма
    :param recipient:
    :param username:
    :param verify_url:
    :return:
    """
    html = render_html(
        "verify.html",
        context={"username": username, "verify_url": verify_url},
    )
    send_email(
        recipients=[recipient],
        subject="Verify Email",
        html_content=html,
    )
