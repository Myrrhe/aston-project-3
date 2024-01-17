"""The urls file."""
from django.urls import path
from apps.game.views import (
    BotDeletedViewSet,
    BotMatchDataViewSet,
    BotMatchesViewSet,
    BotMatchViewSet,
    CreateBotViewSet,
    DeleteBotViewSet,
    DuplicateBotViewSet,
    EditBotViewSet,
    MyBotsViewSet,
    TogglePublishBotViewSet,
)

app_name = "game"

urlpatterns = [
    path(
        "bots/my-bots",
        MyBotsViewSet.as_view(),
        name="my-bots",
    ),
    path(
        "bots/bot-matches/<uuid:bot_id>",
        BotMatchesViewSet.as_view(),
        name="bot-matches",
    ),
    path(
        "bots/bot-matches/<uuid:bot_id>/<uuid:match_id>",
        BotMatchViewSet.as_view(),
        name="bot-match",
    ),
    path(
        "bots/bot-matches-data/<uuid:bot_id>/<uuid:match_id>",
        BotMatchDataViewSet.as_view(),
        name="bot-match-data",
    ),
    path(
        "bots/new",
        CreateBotViewSet.as_view(),
        name="create-bot",
    ),
    path(
        "bots/edit/<uuid:bot_id>",
        EditBotViewSet.as_view(),
        name="edit-bot",
    ),
    path(
        "bots/duplicate",
        DuplicateBotViewSet.as_view(),
        name="duplicate-bot",
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
    path(
        "bots/toggle-publish/<uuid:bot_id>",
        TogglePublishBotViewSet.as_view(),
        name="bot-toggle-publish",
    ),
]
