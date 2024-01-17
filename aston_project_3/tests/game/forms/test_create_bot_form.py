"""The tests for the password change form"""
from django.test import TransactionTestCase

from apps.account.models import User
from apps.game.forms import CreateBotForm
from apps.game.models import Bot


class TestCreateBotForm(TransactionTestCase):
    """The tests for the password change form"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.user = User.objects.create_user(
            "create_bot_form@test.com", password="123456"
        )
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.form = CreateBotForm(
            {
                "name": "new_name_1",
                "code": "# Some code",
            },
            user=self.user
        )
        self.assertIsNone(self.form.bot_id)
        self.form.is_valid()
        self.assertEqual(self.form.clean(), {
            "name": "new_name_1",
            "code": "# Some code",
        })
        self.form.save(False)
        self.assertEqual(Bot.objects.count(), 0)
        bot = self.form.save(True)
        self.assertEqual(Bot.objects.count(), 1)

        self.form = CreateBotForm(
            {
                "name": "new_name_2",
                "code": "# Some other code",
            },
            user=self.user,
            bot_id=bot.id
        )
        self.assertEqual(self.form.bot_id, bot.id)
        self.form.is_valid()
        self.form.clean()
        self.form.save(False)
        self.assertEqual(Bot.objects.all()[0].name, "new_name_1")
        self.form.save(True)
        self.assertEqual(Bot.objects.all()[0].name, "new_name_2")
