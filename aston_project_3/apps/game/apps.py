"""The app file."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GameConfig(AppConfig):
    """The config class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.game"
    verbose_name = _("bot_management")
