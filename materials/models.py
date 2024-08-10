from django.db import models


class Course(models.Model):
    """модель для курса"""

    title = models.TextField(
        verbose_name="Название курса", help_text="Введите название курмп"
    )
    description = models.TextField(
        verbose_name="Описание курса", help_text="Введите описание курса"
    )
    preview = models.ImageField(verbose_name="Превью")

    created_at = models.DateTimeField(
        verbose_name="Дата/время создания", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата/время обновления", auto_now=True
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """модель для занятия"""

    title = models.TextField(
        verbose_name="Название", help_text="Введите название урока"
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание урока"
    )
    preview = models.ImageField(verbose_name="Превью")
    video_url = models.URLField(
        max_length=200, verbose_name="Ссылка на видео", null=True, blank=True
    )
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Курс"
    )

    created_at = models.DateTimeField(
        verbose_name="Дата/время создания", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата/время обновления", auto_now=True
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
