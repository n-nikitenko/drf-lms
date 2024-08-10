from django.contrib.auth.models import AbstractUser
from django.db import models


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

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
