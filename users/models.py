from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    """модель для пользователя для авторизации по email"""

    username = None
    email = models.EmailField(
        unique=True, verbose_name="email", help_text="Укажите адрес электронной почты"
    )
    avatar = models.ImageField(
        upload_to="users",
        verbose_name="аватар",
        null=True,
        blank=True,
        help_text="Загрузите аватар",
    )
    phone = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="номер телефона",
        help_text="Укажите номер телефона",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def is_moderator(self):
        return self.groups.filter(name="moderators").exists()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """модель для платежей"""

    CASH = "CASH"
    TRANSFER = "TRANSFER"
    PAYMENT_METHOD_CHOICES = ((CASH, "Наличные"), (TRANSFER, "Перевод"))

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payments",
    )

    created_at = models.DateTimeField(
        verbose_name="Дата/время оплаты", auto_now_add=True
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
        related_name="payments",
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
        related_name="payments",
    )

    value = models.PositiveIntegerField(verbose_name="Сумма оплаты")

    method = models.CharField(
        choices=PAYMENT_METHOD_CHOICES, max_length=200, verbose_name="Метод оплаты"
    )

    def __str__(self):
        return f"Сумма: {self.value}, метод: {self.get_method_display()}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
