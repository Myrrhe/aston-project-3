"""The tests for the bot matches view."""
from importlib import import_module

from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpRequest
from django.test import TransactionTestCase

from apps.account.models import User
from apps.game.models import Bot
from apps.game.views import BotMatchesViewSet


class TestBotMatchesView(TransactionTestCase):
    """The tests for the bot matches view."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.request = HttpRequest()
        self.request.method = "GET"
        self.request.path = "/fr-fr/login/"
        self.request.session = None
        self.user_1 = User.objects.create_user(
            "bot_matches_view_1@test.com", "123456"
        )
        self.user_2 = User.objects.create_user(
            "bot_matches_view_2@test.com", "123456"
        )
        self.bot = Bot.objects.create(
            user=self.user_1,
            name="test_bot",
            posted=False,
            score=0,
        )
        self.request.user = self.user_2

        self.request.session = import_module(settings.SESSION_ENGINE).SessionStore()

        self.view = BotMatchesViewSet()
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(self.view.get(self.request, self.bot.id).status_code, 302)
        self.request.user = self.user_1
        self.assertEqual(self.view.get(self.request, self.bot.id).status_code, 200)
        logout(self.request)
        self.assertEqual(self.view.get(self.request, self.bot.id).status_code, 302)
