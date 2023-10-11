"""The app file"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """The config class"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
