from django.db import models
from django.utils import timezone


class BlogPost(models.Model):
    """Модель блоговой записи"""

    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок"
    )
    content = models.TextField(
        verbose_name="Содержимое"
    )
    preview = models.ImageField(
        upload_to='blog_previews/',
        blank=True,
        null=True,
        verbose_name="Превью (изображение)"
    )
    created_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата создания"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано"
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество просмотров",
    )

    class Meta:
        verbose_name = "блоговая запись"
        verbose_name_plural = "блоговые записи"
        ordering = ['-created_date']  # сортировка: сначала новые

    def __str__(self):
        return self.title