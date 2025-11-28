from core.celery import app
from core.config import conf

from .common import render_html, send_email


@app.task
def welcome_email(
    recipient: str,
    username: str,
):
    """
    Задача по отправке письма при регистрации нового пользователя
    :param recipient: user email
    :param username: username
    :return:
    """
    html = render_html(
        "welcome.html", context={"base_url": conf.frontend.url, "username": username}
    )
    send_email(
        recipients=[recipient],
        subject="Welcome Email",
        html_content=html,
    )
