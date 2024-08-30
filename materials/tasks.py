from smtplib import SMTPSenderRefused

from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


@shared_task
def send_notification_task(mail, course_name):
    """Отправка уведомления об обновлении курса на указанный email"""
    try:
        send_mail(
            "Уведомление об обновлении курса",
            f"Курс '{course_name}' обновлен.",
            EMAIL_HOST_USER,
            [mail],
            fail_silently=False,
        )
    except SMTPSenderRefused as e:
        pass
