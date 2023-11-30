"""The post's model."""

import uuid

from django.db import models
from django.utils.translation import gettext as _

from apps.account.models import User
from apps.core.models import TimestampedModel
from apps.forum.models import Topic


class Post(TimestampedModel):
    """The post's model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("user"),
        help_text=_("user_of_post_help_text"),
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.PROTECT,
        verbose_name=_("topic"),
        help_text=_("topic_of_post_help_text"),
    )
    content = models.TextField(
        max_length=4096,
        null=True,
        blank=True,
        verbose_name=_("content"),
        help_text=_("content_help_text"),
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

        db_table = "post"
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self) -> str:
        """Represent the class objects as a string."""
        return f"{self.topic.title} : {self.user}"
