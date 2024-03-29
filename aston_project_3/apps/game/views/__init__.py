"""The module file."""
from .bot_deleted_view import BotDeletedViewSet
from .bot_matches_view import BotMatchesViewSet
from .bot_match_data_view import BotMatchDataViewSet
from .bot_match_view import BotMatchViewSet
from .create_bot_view import CreateBotViewSet
from .delete_bot_view import DeleteBotViewSet
from .duplicate_bot_view import DuplicateBotViewSet
from .edit_bot_view import EditBotViewSet
from .my_bots_view import MyBotsViewSet
from .toggle_publish_bot_view import TogglePublishBotViewSet


__all__ = [
    "BotDeletedViewSet",
    "BotMatchesViewSet",
    "BotMatchViewSet",
    "CreateBotViewSet",
    "DeleteBotViewSet",
    "DuplicateBotViewSet",
    "EditBotViewSet",
    "MyBotsViewSet",
    "TogglePublishBotViewSet",
]
