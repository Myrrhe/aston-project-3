"""The topic section's model."""
import uuid

from django.db import models
from django.utils.translation import gettext as _

from apps.core.models import TimestampedModel


class TopicSection(TimestampedModel):
    """The topic section's model."""

    SECTION_CHOICES = [
        ("bug", "Feedback & Bugs"),
        ("bot", "Bot programming"),
    ]

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
        verbose_name=_("name"),
        help_text=_("name_help_text"),
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

    def natural_key(self) -> tuple[str, ...]:
        """Create a natural key."""
        return (self.code,)

    def __str__(self) -> str:
        """Represent the class objects as a string."""
        return f"{self.name} ({self.code})"

    @classmethod
    def get_all(cls: "TopicSection") -> list[tuple[str, ...]]:
        """Get all the sections as an iterable of 2-tuples."""
        # Warning : This bit of code may cause an error during migrations
        return [(section.code, section.name) for section in cls.objects.all()]
