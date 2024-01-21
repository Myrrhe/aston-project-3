"""The match's model."""
from __future__ import annotations
import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext as _

from apps.core.models import TimestampedModel
from apps.game.models import Bot
from apps.game.utils.bot_fight_util import main_fight


class MatchManager(models.Manager):
    """Custom manager for the bot model."""

    def bot_fight(self, bot_left: Bot, bot_right: Bot, friendly=True) -> Match:
        """Create a match between two bots."""
        res = main_fight([bot_left.id, bot_right.id])
        win = res["result"] == "1"
        match = Match(
            bot_left=bot_left,
            bot_right=bot_right,
            movements=res["movements"],
            result=res["result"] == "1",
            output_left=res["stdout"][0],
            output_right=res["stdout"][1],
            error_messages_left=res["stderr"][0],
            error_messages_right=res["stderr"][1],
        )
        if not friendly:
            match.score_change_left = 1 if win else -1
            match.score_change_right = -1 if win else 1
        match.save()
        bot_left.score += match.score_change_left
        bot_left.save()
        bot_right.score += match.score_change_right
        bot_right.save()
        return match

    def start_match(self) -> None:
        """Start a match between two random bots."""
        bot_left = Bot.objects.order_by("?").first()
        bot_right = Bot.objects.exclude(id=bot_left.id).order_by("?").first()
        self.bot_fight(bot_left, bot_right)

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
    score_change_left = models.IntegerField(
        null=False,
        blank=False,
        default=0,
        verbose_name=_("score_change_left"),
        help_text=_("score_change_left_help_text"),
    )
    score_change_right = models.IntegerField(
        null=False,
        blank=False,
        default=0,
        verbose_name=_("score_change_right"),
        help_text=_("score_change_right_help_text"),
    )
    output_left = ArrayField(
        models.CharField(max_length=1024, blank=True, null=True),
        null=True,
        size=None,
        verbose_name=_("output_left"),
        help_text=_("output_left_help_text"),
    )
    output_right = ArrayField(
        models.CharField(max_length=1024, blank=True, null=True),
        null=True,
        size=None,
        verbose_name=_("output_right"),
        help_text=_("output_right_help_text"),
    )
    error_messages_left = ArrayField(
        ArrayField(
            models.CharField(max_length=1024, blank=True, null=True),
            null=True,
            size=None,
        ),
        null=True,
        verbose_name=_("stderr_left"),
        help_text=_("stderr_left_help_text"),
    )
    error_messages_right = ArrayField(
        ArrayField(
            models.CharField(max_length=1024, blank=True, null=True),
            null=True,
            size=None,
        ),
        null=True,
        size=None,
        verbose_name=_("stderr_right"),
        help_text=_("stderr_right_help_text"),
    )

    def save(self, *args, **kwargs):
        """Save the model in the database (overidden to pad the arrays)."""
        if self.error_messages_left:
            max_length_left = max(len(row) for row in self.error_messages_left)
            self.error_messages_left = [row + [None] * (max_length_left - len(row)) for row in self.error_messages_left]
        if self.error_messages_right:
            max_length_right = max(len(row) for row in self.error_messages_right)
            self.error_messages_right = [row + [None] * (max_length_right - len(row)) for row in self.error_messages_right]
        super().save(*args, **kwargs)

    REQUIRED_FIELDS = []

    objects = MatchManager()

    class Meta(TimestampedModel.Meta):
        """The meta class."""

        db_table = "match"
        verbose_name = _("match")
        verbose_name_plural = _("matchs")

    def am_i_the_bad_guy(self, bot: Bot) -> bool:
        if bot.id == self.bot_left.id:
            return True
        elif bot.id == self.bot_right.id:
            return False
        else:
            raise ValueError("This bot didn't fought in this match")

    def get_opponent(self, bot: Bot) -> Bot:
        return self.bot_right if self.am_i_the_bad_guy(bot) else self.bot_left

    def get_result(self, bot: Bot) -> bool:
        return self.result == self.am_i_the_bad_guy(bot)

    def get_score_change(self, bot: Bot) -> int:
        return self.score_change_right if self.am_i_the_bad_guy(bot) else self.score_change_left

    def __str__(self) -> str:
        """Represent the class objects as a string."""
        return f"{self.bot_left} vs {self.bot_right}"
