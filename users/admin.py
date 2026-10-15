from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Админка для кастомного User"""

    list_display = ["id", "email", "is_staff", "is_superuser", "is_active"]
    list_filter = ["is_staff", "is_superuser", "is_active", "groups"]
    list_display_links = ["id", "email"]
    search_fields = ["email"]
    ordering = ["id"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональная информация", {"fields": ("first_name", "last_name")}),
        (
            "Права",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
