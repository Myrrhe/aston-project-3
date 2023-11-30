"""The topic section's model."""

import uuid

from django.db import models
from django.utils.translation import gettext as _

from apps.core.models import TimestampedModel


class TopicSection(TimestampedModel):
    """The topic section's model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(
        max_length=64,
        default=False,
        null=False,
        blank=False,
        verbose_name=_("code"),
        help_text=_("code_help_text"),
    )
    name = models.CharField(
        max_length=64,
        default=False,
        null=False,
        blank=False,
        verbose_name=_("deleted"),
        help_text=_("deleted_help_text"),
    )
    description = models.TextField(
        max_length=4096,
        default=False,
        null=False,
        blank=False,
        verbose_name=_("description"),
        help_text=_("description_help_text"),
    )

    REQUIRED_FIELDS = []

    class Meta(TimestampedModel.Meta):
        """The meta class."""

        db_table = "topic_section"
        verbose_name = _("topic_section")
        verbose_name_plural = _("topic_sections")

    def __str__(self) -> str:
        """Represent the class objects as a string."""
        return f"{self.name} ({self.code})"
