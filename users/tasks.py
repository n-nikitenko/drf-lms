from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def block_inactive_users():
    users = User.objects.all()
    for user in users:
        start_date = user.last_login or user.date_joined
        delta = timezone.now() - start_date
        if delta > timezone.timedelta(days=30):
            user.is_active = False
            user.save()
