"""The tests for the bot model"""
import os

from django.test import TransactionTestCase

from apps.account.models import User
from apps.game.models import Bot


class TestBotModel(TransactionTestCase):
    """The tests for the bot model"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.user = User.objects.create_superuser(
            "bot_model@test.com", "123456"
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
        self.assertEqual(Bot.objects.get_default_code, "\
import sys\n\
import math\n\
\n\
\n\
# game loop\n\
while True:\n\
    # p: your player number (0 to 1).\n\
    p = int(input())\n\
    for i in range(2):\n\
        # x0: starting X coordinate of lightcycle (or -1)\n\
        # y0: starting Y coordinate of lightcycle (or -1)\n\
        # x1: starting X coordinate of lightcycle (can be the same as X0 if you play before this player)\n\
        # y1: starting Y coordinate of lightcycle (can be the same as Y0 if you play before this player)\n\
        x0, y0, x1, y1 = [int(j) for j in input().split()]\n\
\n\
    # A single line with UP, DOWN, LEFT or RIGHT\n\
    print(\"LEFT\")\n\
")

        self.assertEqual(
            Bot.objects.get_by_natural_key(self.user.email, self.bot.name).id,
            self.bot.id
        )
        self.assertEqual(self.bot.natural_key(), (self.user, self.bot.name,))
        self.assertEqual(str(self.bot), f"{self.bot.name} [{self.user}]")
        self.assertFalse(self.bot.load_script())
        if not os.path.exists(f"apps/game/bot_scripts/{self.bot.id}"):
            os.makedirs(f"apps/game/bot_scripts/{self.bot.id}")
        with open(
            f"apps/game/bot_scripts/{self.bot.id}/script.py",
            "w",
            encoding="utf-8"
        ) as file_code_bot:
            file_code_bot.write(Bot.objects.get_default_code)
        self.assertTrue(self.bot.load_script())
        self.assertEqual(self.bot.get_code, Bot.objects.get_default_code)
        try:
            os.remove(f"apps/game/bot_scripts/{self.bot.id}/script.py")
        except FileNotFoundError:
            print(f"Le fichier apps/game/bot_scripts/{self.bot.id}/script.py n'a pas été trouvé.")
        try:
            os.rmdir(f"apps/game/bot_scripts/{self.bot.id}")
        except FileNotFoundError:
            print(f"Le répertoire apps/game/bot_scripts/{self.bot.id} n'a pas été trouvé.")
        except OSError as e:
            print(f"Une erreur s'est produite lors de la suppression du répertoire : {e}")
        try:
            os.remove(f"storage/bot/{self.bot.id}.py")
        except FileNotFoundError:
            print(f"Le fichier storage/bot/{self.bot.id}.py n'a pas été trouvé.")
