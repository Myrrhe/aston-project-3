"""The tests for the delete bot view."""
from django.http import HttpRequest
from django.test import TransactionTestCase
from django.urls import reverse_lazy

from apps.account.models import User
from apps.game.models import Bot
from apps.game.views import DeleteBotViewSet


class TestDeleteBotView(TransactionTestCase):
    """The tests for the delete bot view."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        user = User.objects.create_user("delete_bot_view@test.com", "123456")
        self.view = DeleteBotViewSet()
        self.view.request = HttpRequest()
        self.view.request.method = "POST"
        self.view.request.user = user
        self.bot = Bot.objects.create(
            user=user,
            name="bot_test",
            posted=False,
            score=0,
        )
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(self.view.get(self.view.request, self.bot.id).status_code, 200)
        self.assertEqual(
            self.view.get_form_kwargs(),
            {
                "initial": {},
                "prefix": None,
                "data": {},
                "files": {},
                "user": self.view.request.user,
            },
        )
        context_data = self.view.get_context_data()
        context_data["form"] = self.view.form_class(
            {
                "bot_id": self.bot.id,
            },
            user=self.view.request.user,
        )
        self.assertTrue(context_data["form"].is_valid())
        self.assertEqual(self.view.form_valid(context_data["form"]).status_code, 302)
        self.assertEqual(Bot.objects.count(), 0)
        self.assertEqual(
            self.view.get_success_url(), reverse_lazy("game:bot-deleted")
        )
