"""The app file"""
from django.apps import AppConfig


class AccountConfig(AppConfig):
    """The config class"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.account"
    verbose_name = "Users management"
