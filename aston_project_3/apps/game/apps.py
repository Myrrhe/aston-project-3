"""The app file."""
import os
from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.game.scripts import ScriptManager


class GameConfig(AppConfig):
    """The config class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.game"
    verbose_name = _("bot_management")

    def ready(self):
        # OS here is to prevent the manager from being called twice
        if settings.MATCH_AUTO == "1" and os.environ.get("RUN_MAIN") == None:
            ScriptManager.start_external_script()
