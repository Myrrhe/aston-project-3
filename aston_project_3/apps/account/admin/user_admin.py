"""The user's admin."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from apps.account.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """The user's admin."""

    list_display = (
        "email",
        "is_admin",
        "is_superuser",
    )
    fieldsets = (
        (
            _("personal_info"),
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            _("additionnal_info"),
            {"fields": ("username",)},
        ),
        (
            _("permissions"),
            {
                "fields": (
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("informations"), {"fields": ("last_login",)}),
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
