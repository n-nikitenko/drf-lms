from django.conf import settings
from django.db import models

from materials.services import send_notifications


class Course(models.Model):
    """модель для курса"""

    title = models.TextField(
        verbose_name="Название курса", help_text="Введите название курса"
    )
    description = models.TextField(
        verbose_name="Описание курса",
        help_text="Введите описание курса",
        null=True,
        blank=True,
    )
    preview = models.ImageField(verbose_name="Превью", null=True, blank=True)

    created_at = models.DateTimeField(
        verbose_name="Дата/время создания", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата/время обновления", auto_now=True
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Автор",
        related_name="courses",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        send_notifications(self)

    class Meta:
        ordering = ["id"]
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """модель для занятия"""

    title = models.TextField(
        verbose_name="Название", help_text="Введите название урока"
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание урока",
        null=True,
        blank=True,
    )
    preview = models.ImageField(verbose_name="Превью", null=True, blank=True)
    video_url = models.URLField(
        max_length=200, verbose_name="Ссылка на видео", null=True, blank=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Курс",
        related_name="lessons",
    )

    created_at = models.DateTimeField(
        verbose_name="Дата/время создания", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата/время обновления", auto_now=True
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Автор",
        related_name="lessons",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        if self.course:
            send_notifications(self.course)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["id"]


class Subscription(models.Model):
    """модель подписки пользователя на курс"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscriptions",
    )

    def __str__(self):
        return f"Подписка пользователя {self.user} на курс '{self.course}'"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
