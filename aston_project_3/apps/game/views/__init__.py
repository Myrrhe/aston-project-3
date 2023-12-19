"""The module file."""
from .bot_deleted_view import BotDeletedViewSet
from .create_bot_view import CreateBotViewSet
from .delete_bot_view import DeleteBotViewSet
from .edit_bot_view import EditBotViewSet
from .my_bots_view import MyBotsViewSet


__all__ = [
    "BotDeletedViewSet",
    "CreateBotViewSet",
    "DeleteBotViewSet",
    "EditBotViewSet",
    "MyBotsViewSet",
]
