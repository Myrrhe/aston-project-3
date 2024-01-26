"""The tests for the bot match view."""
from importlib import import_module

from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpRequest
from django.test import TransactionTestCase

from apps.account.models import User
from apps.game.models import Bot, Match
from apps.game.views import BotMatchDataViewSet


class TestBotMatchDataView(TransactionTestCase):
    """The tests for the bot match view."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.request = HttpRequest()
        self.request.method = "GET"
        self.request.path = "/fr-fr/login/"
        self.request.session = None
        self.user_1 = User.objects.create_user(
            "bot_match_data_view_1@test.com", "123456"
        )
        self.user_2 = User.objects.create_user(
            "bot_match_data_view_2@test.com", "123456"
        )
        self.bot_left = Bot.objects.create(
            user=self.user_1,
            name="bot_left",
            posted=False,
            score=0,
        )
        self.bot_right = Bot.objects.create(
            user=self.user_1,
            name="bot_right",
            posted=False,
            score=0,
        )
        self.bot_bystander = Bot.objects.create(
            user=self.user_1,
            name="bot_bystander",
            posted=False,
            score=0,
        )
        self.match = Match.objects.create(
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

        self.request.user = self.user_2
        self.request.session = import_module(settings.SESSION_ENGINE).SessionStore()

        self.view = BotMatchDataViewSet()
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(self.view.get(
            self.request,
            self.bot_left.id,
            self.match.id
        ).status_code, 403)
        self.request.user = self.user_1
        self.assertEqual(self.view.get(
            self.request,
            self.bot_bystander.id,
            self.match.id
        ).status_code, 403)
        self.assertEqual(self.view.get(
            self.request,
            self.bot_left.id,
            self.match.id
        ).status_code, 200)
        logout(self.request)
        self.assertEqual(self.view.get(
            self.request,
            self.bot_left.id,
            self.match.id
        ).status_code, 403)
