from django.contrib import admin

from catalog.models import Category, Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name", "description")
