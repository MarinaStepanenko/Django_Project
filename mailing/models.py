from datetime import timezone

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=200, verbose_name="Ф.И.О")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="recipients",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели рассылки"
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Message(models.Model):
    subject = models.CharField(max_length=200, verbose_name="Тема письма")
    text_body = models.TextField(verbose_name="Тело письма")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["subject"]

    def __str__(self):
        return self.subject


class Mailing(models.Model):

    STATUS_CREATED = "Создана"
    STATUS_STARTED = "Запущена"
    STATUS_FINISHED = "Завершена"

    STATUS_CHOICES = [
        (STATUS_CREATED, "Создана"),
        (STATUS_STARTED, "Запущена"),
        (STATUS_FINISHED, "Завершена"),
    ]

    start_time = models.DateTimeField(verbose_name="Дата и время начала отправки")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
        verbose_name="Статус",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        related_name="mailings",
    )
    recipients = models.ManyToManyField(
        Recipient, verbose_name="Получатели", related_name="mailings"
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-start_time"]

    def __str__(self):
        return f"Рассылка №{self.pk}: {self.start_time:%d.%m.%Y %H:%M} - {self.end_time:%d.%m.%Y %H:%M}"

    def clean(self):
        now = timezone.now()

        if self.start_time < now:
            raise ValidationError(
                {"start_time": "Дата начала рассылки не может быть в прошлом"}
            )
        if self.end_time and self.start_time and self.end_time <= self.start_time:
            raise ValidationError(
                {"end_time": "Дата окончания рассылки не может быть раньше даты начала"}
            )

    def update_status(self):
        """
        Он будет проверять текущее время и сравнивать его с
        датой начала и датой окончания рассылки.
        Если текущий статус в базе отличается от вычисленного
        (нового), метод обновит статус в базе данных.
        Это позволит статусу меняться автоматически, без участия пользователя.
        """
        now = timezone.now()

        if now < self.start_time:
            new_status = self.STATUS_CREATED
        elif self.start_time <= now <= self.end_time:
            new_status = self.STATUS_CREATED
        else:
            new_status = self.STATUS_FINISHED

        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=["status"])


class MailingAttempt(models.Model):

    STATUS_SUCCESS = "Успешно"
    STATUS_FAILED = "Не успешно"

    STATUS_CHOICES = [
        (STATUS_SUCCESS, "Успешно"),
        (STATUS_FAILED, "Не успешно"),
    ]

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name="Рассылка",
        related_name="attempts",
    )

    attempt_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время рассылки"
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, verbose_name="Статус"
    )

    server_response = models.TextField(
        blank=True, null=True, verbose_name="Ответ сервера"
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["-attempt_time"]

    def __str__(self):
        return f"{self.mailing} - {self.status} ({self.attempt_time:%d.%m.%Y %H:%M})"
