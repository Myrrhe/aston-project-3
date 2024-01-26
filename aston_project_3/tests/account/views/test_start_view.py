"""The tests for the start view."""
from django.http import HttpRequest
from django.test import TransactionTestCase

from apps.account.models import User
from apps.account.views import StartViewSet
from apps.game.models import Bot, Match


class TestStartView(TransactionTestCase):
    """The tests for the start view."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.request = HttpRequest()
        self.request.method = "GET"
        self.request.session = None
        self.request.user = User.objects.create_user(
            "start_view@test.com", "123456"
        )

        self.bot_left = Bot.objects.create(
            user=self.request.user,
            name="bot_left",
            posted=False,
            score=0,
        )
        self.bot_right = Bot.objects.create(
            user=self.request.user,
            name="bot_right",
            posted=False,
            score=0,
        )

        self.view = StartViewSet()
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(self.view.get(self.request).status_code, 200)
        Match.objects.create(
            bot_left=self.bot_left,
            bot_right=self.bot_right,
            movements="",
            result=True,
            score_change_left=-1,
            score_change_right=1,
            output_left=[],
            output_right=[],
            error_messages_left=[],
            error_messages_right=[],
        )
        self.assertEqual(self.view.get(self.request).status_code, 200)
