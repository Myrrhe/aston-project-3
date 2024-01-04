"""The bot's admin."""
from django.contrib import admin

from apps.game.models import Bot


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    """The user's admin."""

    list_display = (
        "user",
        "name",
        "score",
        "posted",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "name",
                    "score",
                    "posted",
                )
            },
        ),
    )
    search_fields = [
        "email",
    ]
    ordering = ("user", "name", "score")
    list_filter = (
        "posted",
    )
    select_related = True
