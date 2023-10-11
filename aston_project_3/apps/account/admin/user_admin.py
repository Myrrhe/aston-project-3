"""The user's admin"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.account.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """The user's admin"""

    list_display = (
        "email",
        "is_admin",
        "is_superuser",
    )
    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Informations", {"fields": ("last_login",)}),
        (
            None,
            {
                "fields": (
                    "is_email_confirmed",
                    "is_tou_accepted",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_admin",
                ),
            },
        ),
    )
    search_fields = [
        "email",
    ]
    ordering = ("email",)
    list_filter = (
        "is_admin",
        "is_superuser",
    )
    select_related = True
