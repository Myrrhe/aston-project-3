"""The tests for the delete bot duplication view."""
import os

from django.http import HttpRequest
from django.test import TransactionTestCase
from django.urls import reverse_lazy
from werkzeug.utils import secure_filename

from apps.account.models import User
from apps.game.models import Bot
from apps.game.views import DuplicateBotViewSet


class TestDuplicateBotView(TransactionTestCase):
    """The tests for the bot duplication view."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.user = User.objects.create_user("duplicate_bot_view@test.com", "123456")
        self.view = DuplicateBotViewSet()
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
        with open("storage/bot/" + secure_filename(
            f"{self.bot.id}.py"), "w", newline="", encoding="utf-8"
        ) as file:
            file.write(Bot.objects.get_default_code)
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
        # print(self.view.get_context_data())
        self.assertEqual(self.view.post(self.view.request).status_code, 302)
        self.assertEqual(Bot.objects.count(), 1)
        self.view.bot_id = self.bot.id
        self.assertEqual(
            self.view.get_success_url(),
            reverse_lazy("game:edit-bot", args=[self.view.bot_id])
        )
        self.view.request.POST = {
            "duplicate_bot_form-bot_id": self.bot.id,
            "duplicate_bot_form": "duplicate_bot",
        }
        self.assertEqual(self.view.post(self.view.request).status_code, 302)
        self.assertEqual(Bot.objects.count(), 2)

        try:
            os.remove(f"storage/bot/{self.bot.id}.py")
        except FileNotFoundError:
            print(f"Le fichier storage/bot/{self.bot.id}.py n'a pas été trouvé.")
        try:
            os.remove(f"storage/bot/{self.view.bot_id}.py")
        except FileNotFoundError:
            print(f"Le fichier storage/bot/{self.view.bot_id}.py n'a pas été trouvé.")
