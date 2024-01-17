"""The tests for the password change form"""
from pathlib import Path

from django.test import TransactionTestCase

from apps.account.models import User
from apps.game.forms import DeleteBotForm
from apps.game.models import Bot


class TestDeleteBotForm(TransactionTestCase):
    """The tests for the password change form"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.user = User.objects.create_user(
            "create_bot_form@test.com", password="123456"
        )
        self.bot_1 = Bot.objects.create(
            user=self.user,
            name="bot_test_1",
            posted=False,
            score=0,
        )
        self.bot_2 = Bot.objects.create(
            user=self.user,
            name="bot_test_2",
            posted=False,
            score=0,
        )
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        form = self.form = DeleteBotForm(
            {
                "bot_id": self.bot_1.id,
            },
            user=self.user
        )
        self.assertEqual(form.user.email, self.user.email)
        with open(f"storage/bot/{self.bot_2.id}.py", "w") as file_code_bot:
            file_code_bot.write(Bot.objects.get_default_code)
        form.is_valid()
        self.assertEqual(form.clean(), {"bot_id": self.bot_1.id})
        form.delete_bot()
        self.assertEqual(Bot.objects.count(), 1)
        form = self.form = DeleteBotForm(
            {
                "bot_id": self.bot_2.id,
            },
            user=self.user
        )
        form.is_valid()
        form.clean()
        form.delete_bot()
        self.assertFalse(Path(f"storage/bot/{self.bot_2.id}.py").exists())
