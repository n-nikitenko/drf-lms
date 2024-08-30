from materials.tasks import send_notification_task


def send_notifications(course: "Course"):
    """отправка уведомлений всем пользователям, подписанным на курс"""
    for subscription in course.subscription_set.all():
        send_notification_task.delay(subscription.user.email, course.title)
