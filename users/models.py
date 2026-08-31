from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = PhoneNumberField(
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона в международном формате",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Фотография",
        blank=True,
        null=True,
        help_text="Загрузите вашу фотографию",
    )
    country = models.CharField(
        max_length=20,
        verbose_name="Страна",
        blank=True,
        null=True,
        help_text="Укажите вашу страну",
    )
    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
