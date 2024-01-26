"""The module file."""
from .test_bot_deleted_view import TestBotDeletedView
from .test_bot_match_data_view import TestBotMatchDataView
from .test_bot_match_view import TestBotMatchView
from .test_bot_matches_view import TestBotMatchesView
from .test_create_bot_view import TestCreateBotView
from .test_delete_bot_view import TestDeleteBotView
from .test_duplicate_bot_view import TestDuplicateBotView
from .test_my_bots_view import TestMyBotsView
from .test_toggle_publish_bot_view import TestTogglePublishBotView

__all__ = [
    "TestBotDeletedView",
    "TestBotMatchDataView",
    "TestBotMatchView",
    "TestBotMatchesView",
    "TestCreateBotView",
    "TestDeleteBotView",
    "TestDuplicateBotView",
    "TestTogglePublishBotView",
    "TestMyBotsView",
]
