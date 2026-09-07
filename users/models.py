from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # 1. Устанавливаем права администратора
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # 2. Вызываем create_user с этими правами
        return self.create_user(email, password, **extra_fields)


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

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
