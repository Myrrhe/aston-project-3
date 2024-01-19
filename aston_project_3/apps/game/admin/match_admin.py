"""The bot's admin."""
from django.contrib import admin

from apps.game.models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    """The match's admin."""

    list_display = (
        "bot_left",
        "bot_right",
        "result",
        "created_at",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "bot_left",
                    "bot_right",
                    "movements",
                    "result",
                    "score_change_left",
                    "score_change_right",
                    "output_left",
                    "output_right",
                    "error_messages_left",
                    "error_messages_right",
                )
            },
        ),
    )
    search_fields = [
        "bot_left",
        "bot_right",
    ]
    ordering = ("bot_left", "bot_right", "created_at")
    list_filter = (
        "result",
    )
    select_related = True
