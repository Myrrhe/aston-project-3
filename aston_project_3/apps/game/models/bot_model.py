"""The bot's model."""
import shutil
import uuid
from pathlib import Path

from django.db import models
from django.utils.translation import gettext as _
from werkzeug.utils import secure_filename

from apps.account.models import User
from apps.core.models import TimestampedModel


class Bot(TimestampedModel):
    """The bot's model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("user"),
        help_text=_("user_of_bot_help_text"),
    )
    name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name=_("name"),
        help_text=_("name_help_text"),
    )
    posted = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name=_("posted"),
        help_text=_("posted_help_text"),
    )
    score = models.IntegerField(
        null=False,
        blank=False,
        default=0,
        verbose_name=_("score"),
        help_text=_("score_help_text"),
    )

    REQUIRED_FIELDS = []

    class Meta(TimestampedModel.Meta):
        """The meta class."""

        db_table = "bot"
        verbose_name = _("bot")
        verbose_name_plural = _("bots")

    @property
    def get_code(self) -> str:
        """Return the Python script of the bot."""
        with open("storage/bot/" + secure_filename(f"{self.id}.py"), encoding="utf-8") as f:
            res = f.read()
        return res

    def load_script(self) -> None:
        """Copy the script of the bot into storage."""
        if Path(f"apps/game/bot_scripts/{self.id}/script.py").is_file():
            shutil.copy(
                f"apps/game/bot_scripts/{self.id}/script.py",
                f"storage/bot/{self.id}.py",
            )

    def __str__(self) -> str:
        """Represent the class objects as a string."""
        return f"{self.user} : {self.name}"
