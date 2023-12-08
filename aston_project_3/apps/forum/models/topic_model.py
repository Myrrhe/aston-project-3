"""The topic's model."""

import uuid

from django.db import models
from django.utils.translation import gettext as _

from apps.account.models import User
from apps.core.models import TimestampedModel
from apps.forum.models import TopicSection


class Topic(TimestampedModel):
    """The topic's model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("user"),
        help_text=_("user_of_topic_help_text"),
    )
    section = models.ForeignKey(
        TopicSection,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("section"),
        help_text=_("topic_section_of_topic_help_text"),
    )
    title = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("title"),
        help_text=_("title_help_text"),
    )
    content = models.TextField(
        max_length=4096,
        null=True,
        blank=True,
        verbose_name=_("content"),
        help_text=_("content_help_text"),
    )
    views = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=0,
        verbose_name=_("views"),
        help_text=_("views_help_text"),
    )
    deleted = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name=_("deleted"),
        help_text=_("deleted_help_text"),
    )

    REQUIRED_FIELDS = []

    class Meta(TimestampedModel.Meta):
        """The meta class."""

        db_table = "topic"
        verbose_name = _("topic")
        verbose_name_plural = _("topics")

    @property
    def last_activity(self) -> str:
        """Get the date of the last post."""
        return (
            self.posts.latest("created_at").created_at
            if self.posts.count()
            else self.created_at
        )

    @property
    def get_replies(self) -> int:
        """Get the number of posts."""
        return self.posts.count()

    def increment_view(self) -> None:
        """Increment the views by one."""
        self.views += 1
        self.save()

    def __str__(self) -> str:
        """Represent the class objects as a string."""
        return f"{self.title}"
