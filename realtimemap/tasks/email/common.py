import logging
import smtplib
from email.message import EmailMessage
from typing import Optional, List, Dict

from jinja2 import TemplateNotFound

from core.app.templating import TemplateManager
from core.celery import app
from core.config import conf

templates = TemplateManager(conf.template_dir / "emails")

logger = logging.getLogger(__name__)


def render_html(template_name: str, context: Optional[Dict] = None) -> str:
    """
    Возвращает шаблон в виде строки с учетом контекста
    :param template_name: Название файла
    :param context: Контекст
    :return: str
    """
    if context is None:
        context = dict()

    try:
        template = templates.engine.get_template(template_name)
        return template.render(context)
    except TemplateNotFound:
        logger.error("Cannot find template: %s", template_name)
        raise


def send_email(
    recipients: List[str],
    subject: str,
    html_content: str,
    text_content: Optional[str] = None,
    sender_email: str = conf.smtp.admin_email,
) -> None:
    """
    Метод для отправки письма/писем

    :param recipients: Список получателей
    :param subject: Тема письма
    :param html_content: HTML контент письма
    :param text_content: Текстовое наполнение письма
    :param sender_email: Отправитель
    :return: None
    """
    if not recipients:
        logger.warning("Nothing to send")
        return

    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject

    if text_content:
        message.set_content(text_content, subtype="plain")
        message.add_alternative(html_content, subtype="html")
    else:
        message.set_content(html_content, subtype="html")

    try:
        with smtplib.SMTP_SSL(host=conf.smtp.host, port=conf.smtp.port) as smtp:
            smtp.login(conf.smtp.admin_email, conf.smtp.admin_password)
            smtp.send_message(message)
            logger.info("Email sent. Count %d", len(recipients))
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP authentication error")
        raise
    except smtplib.SMTPConnectError:
        logger.error("SMTP connection error")
        raise
    except Exception as e:
        logger.error("Undefined error: %s", e)
        raise


@app.task
def welcome_email(
    recipient: str,
    username: str,
):
    base_url = "https://realtimemap.ru"

    html = render_html(
        "welcome.html", context={"base_url": base_url, "username": username}
    )
    send_email(
        recipients=[recipient],
        subject="Welcome Email",
        html_content=html,
    )
