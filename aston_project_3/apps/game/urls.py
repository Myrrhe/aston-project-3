"""The urls file."""
from django.urls import path
from apps.game.views import (
    BotDeletedViewSet,
    DeleteBotViewSet,
    MyBotsViewSet,
)

app_name = "game"

urlpatterns = [
    path(
        "bots/my-bots",
        MyBotsViewSet.as_view(),
        name="my-bots",
    ),
    path(
        "bots/delete/<uuid:bot_id>",
        DeleteBotViewSet.as_view(),
        name="delete-bot",
    ),
    path(
        "bots/deleted",
        BotDeletedViewSet.as_view(),
        name="bot-deleted",
    ),
]
