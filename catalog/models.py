from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="наименование", help_text="Введите наименование"
    )
    description = models.TextField(
        verbose_name="описание", help_text="Введите описание", blank=True, null=True
    )
    photo = models.ImageField(
        upload_to="catalog/photo",
        blank=True,
        null=True,
        verbose_name="фото",
        help_text="Загрузите изображение продукта",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="категория",
        help_text="Введите категорию",
    )
    price = models.IntegerField(
        verbose_name="цена за покупку", help_text="Введите цену в рублях"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="дата последнего изменения"
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = ["category__name", "price"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="категория", help_text="Введите название категории"
    )
    description = models.TextField(
        verbose_name="описание",
        help_text="Введите описание категории",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="дата последнего изменения"
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name
