"""The app file."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountConfig(AppConfig):
    """The config class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.account"
    verbose_name = _("users_management")
