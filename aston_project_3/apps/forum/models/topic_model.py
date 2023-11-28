"""The topic's model"""

import uuid

from django.db import models
from django.utils.translation import gettext as _

from apps.account.models import User
from apps.core.models import TimestampedModel


class Topic(TimestampedModel):
    """The topic's model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("user"),
        help_text=_("user_of_topic_help_text"),
    )
    title = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name=_("title"),
        help_text=_("title_help_text"),
    )
    post = models.TextField(
        max_length=4096,
        null=False,
        blank=False,
        verbose_name=_("post"),
        help_text=_("post_help_text"),
    )
    section = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name=_("section"),
        help_text=_("section_help_text"),
    )
    views = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name=_("views"),
        help_text=_("views_help_text"),
    )
    deleted = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        verbose_name=_("deleted"),
        help_text=_("deleted_help_text"),
    )

    REQUIRED_FIELDS = []

    class Meta(TimestampedModel.Meta):
        """The meta class"""

        db_table = "topic"
        verbose_name = _("topic")
        verbose_name_plural = _("topics")

    def __str__(self) -> str:
        return f"{self.title}"
