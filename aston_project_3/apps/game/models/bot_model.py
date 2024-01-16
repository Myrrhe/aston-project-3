"""The bot's model."""
from __future__ import annotations
import shutil
import uuid
from pathlib import Path

from django.db import models
from django.utils.translation import gettext as _
from werkzeug.utils import secure_filename

from apps.account.models import User
from apps.core.models import TimestampedModel


class BotManager(models.Manager):
    """Custom manager for the bot model."""

    def get_by_natural_key(self, user_mail: str, name: str) -> Bot:
        """Get a bot by their creator's mail and name."""
        return self.get(name=name, user__email=user_mail)

    @property
    def get_default_code(self) -> Bot:
        return "\
import sys\n\
import math\n\
\n\
\n\
# game loop\n\
while True:\n\
    # p: your player number (0 to 1).\n\
    p = int(input())\n\
    for i in range(2):\n\
        # x0: starting X coordinate of lightcycle (or -1)\n\
        # y0: starting Y coordinate of lightcycle (or -1)\n\
        # x1: starting X coordinate of lightcycle (can be the same as X0 if you play before this player)\n\
        # y1: starting Y coordinate of lightcycle (can be the same as Y0 if you play before this player)\n\
        x0, y0, x1, y1 = [int(j) for j in input().split()]\n\
\n\
    # A single line with UP, DOWN, LEFT or RIGHT\n\
    print(\"LEFT\")\n\
"


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

    objects = BotManager()

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

    def load_script(self) -> bool:
        """Copy the script of the bot into storage."""
        if Path(f"apps/game/bot_scripts/{self.id}/script.py").is_file():
            shutil.copy(
                f"apps/game/bot_scripts/{self.id}/script.py",
                f"storage/bot/{self.id}.py",
            )
            return True
        return False

    def natural_key(self) -> tuple[str, ...]:
        """Create a natural key."""
        return self.user, self.name

    def __str__(self) -> str:
        """Represent the class objects as a string."""
        return f"{self.name} [{self.user}]"
