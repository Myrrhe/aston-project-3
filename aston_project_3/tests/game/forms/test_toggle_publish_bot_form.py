"""The tests for the password change form"""
from django.test import TransactionTestCase

from apps.account.models import User
from apps.game.forms import TogglePublishBotForm
from apps.game.models import Bot


class TestTogglePublishBotForm(TransactionTestCase):
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
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        form = self.form = TogglePublishBotForm(user=self.user)
        self.assertIsNone(form.bot_id)
        form = self.form = TogglePublishBotForm(
            {
                "bot_id": self.bot.id,
            },
            user=self.user,
            bot_id=self.bot.id,
        )
        self.assertEqual(form.bot_id, self.bot.id)
        form.is_valid()
        self.assertEqual(form.clean(), {"bot_id": self.bot.id})
        self.assertTrue(form.toggle_publish().posted)
