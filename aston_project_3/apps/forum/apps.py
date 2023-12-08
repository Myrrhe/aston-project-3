"""The module file."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ForumConfig(AppConfig):
    """The config class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.forum"
    verbose_name = _("discussions_management")
