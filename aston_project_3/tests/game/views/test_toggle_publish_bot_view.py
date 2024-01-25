"""The tests for the delete bot publication view."""
from django.http import HttpRequest
from django.test import TransactionTestCase
from django.urls import reverse_lazy

from apps.account.models import User
from apps.game.models import Bot
from apps.game.views import TogglePublishBotViewSet


class TestTogglePublishBotView(TransactionTestCase):
    """The tests for the bot publication view."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.user = User.objects.create_user("toggle_publish_bot_view@test.com", "123456")
        self.view = TogglePublishBotViewSet()
        self.view.object = None
        self.view.request = HttpRequest()
        self.view.request.method = "POST"
        self.view.request.user = self.user
        self.bot = Bot.objects.create(
            user=self.user,
            name="bot_test",
            posted=False,
            score=0,
        )
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(self.view.bot_id, "")
        self.assertEqual(
            self.view.get_form_kwargs(),
            {
                "initial": {},
                "prefix": None,
                "data": {},
                "files": {},
                "instance": None,
                "user": self.view.request.user,
            },
        )
        self.assertEqual(self.view.post(self.view.request, self.bot.id).status_code, 500)
        self.assertFalse(Bot.objects.get(pk=self.bot.id).posted)
        self.view.bot_id = self.bot.id
        self.assertEqual(
            self.view.get_success_url(),
            reverse_lazy("game:edit-bot", args=[self.view.bot_id])
        )
        self.view.request.POST = {
            "toggle_publish_bot_form-bot_id": self.bot.id,
            "toggle_publish_bot_form": "toggle_publish_bot",
        }
        self.assertEqual(self.view.post(self.view.request, self.bot.id).status_code, 200)
        self.assertTrue(Bot.objects.get(pk=self.bot.id).posted)
