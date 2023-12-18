"""The match's model."""

import uuid

from django.db import models
from django.utils.translation import gettext as _

from apps.game.models import Bot
from apps.core.models import TimestampedModel


class Match(TimestampedModel):
    """The match's model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot_left = models.ForeignKey(
        Bot,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("bot_left"),
        help_text=_("bot_left_of_match_help_text"),
        related_name="matches_as_left",
    )
    bot_right = models.ForeignKey(
        Bot,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("bot_right"),
        help_text=_("bot_right_of_match_help_text"),
        related_name="matches_as_right",
    )
    movements = models.TextField(
        max_length=1024,
        null=True,
        blank=True,
        verbose_name=_("movements"),
        help_text=_("movements_help_text"),
    )
    result = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name=_("result"),
        help_text=_("result_help_text"),
    )

    REQUIRED_FIELDS = []

    class Meta(TimestampedModel.Meta):
        """The meta class."""

        db_table = "match"
        verbose_name = _("match")
        verbose_name_plural = _("matchs")

    def __str__(self) -> str:
        """Represent the class objects as a string."""
        return f"{self.bot_left} vs {self.bot_right}"
