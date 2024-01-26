"""The tests for the password change form"""
import os
from pathlib import Path

from django.test import TransactionTestCase

from apps.account.models import User
from apps.game.forms import DuplicateBotForm
from apps.game.models import Bot


class TestDuplicateBotForm(TransactionTestCase):
    """The tests for the password change form"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.user = User.objects.create_user(
            "create_bot_form@test.com", password="123456"
        )
        self.bot = Bot.objects.create(
            user=self.user,
            name="bot_test_1",
            posted=False,
            score=0,
        )
        with open(f"storage/bot/{self.bot.id}.py", "w", encoding="utf-8") as file_code_bot:
            file_code_bot.write(Bot.objects.get_default_code)
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        form = DuplicateBotForm({"bot_id": self.bot.id}, user=self.user)
        self.assertEqual(form.user.email, self.user.email)
        form.is_valid()
        self.assertEqual(form.clean(), {"bot_id": self.bot.id})
        new_bot_1 = form.duplicate_bot()
        self.assertEqual(new_bot_1.name, "bot_test_1 - Copy")
        self.assertEqual(Bot.objects.count(), 2)
        self.assertTrue(Path(f"storage/bot/{new_bot_1.id}.py").exists())
        new_bot_2 = form.duplicate_bot()
        self.assertEqual(new_bot_2.name, "bot_test_1 - Copy (2)")
        try:
            os.remove(f"storage/bot/{self.bot.id}.py")
        except FileNotFoundError:
            print(f"Le fichier storage/bot/{self.bot.id}.py n'a pas été trouvé.")
        try:
            os.remove(f"storage/bot/{new_bot_1.id}.py")
        except FileNotFoundError:
            print(f"Le fichier storage/bot/{new_bot_1.id}.py n'a pas été trouvé.")
        try:
            os.remove(f"storage/bot/{new_bot_2.id}.py")
        except FileNotFoundError:
            print(f"Le fichier storage/bot/{new_bot_2.id}.py n'a pas été trouvé.")
