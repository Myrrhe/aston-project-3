"""The tests for the bot creation view."""
import os
import random
import uuid
from importlib import import_module

from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpRequest
from django.test import TransactionTestCase
from django.urls import reverse_lazy

from apps.account.models import User
from apps.game.models import Bot
from apps.game.views import CreateBotViewSet


class TestCreateBotView(TransactionTestCase):
    """The tests for the bot creation view."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.view = CreateBotViewSet()
        self.view.request = HttpRequest()
        self.view.request.session = import_module(settings.SESSION_ENGINE).SessionStore()
        self.view.request.method = "GET"
        self.view.request.path = "/fr-fr/login/"
        self.view.request.user = User.objects.create_user(
            "create_bot_view@test.com", "123456"
        )
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(self.view.bot_id, "")
        self.assertEqual(self.view.get(self.view.request).status_code, 200)
        self.assertEqual(
            self.view.get_form_kwargs(),
            {
                "initial": {},
                "prefix": None,
                "user": self.view.request.user
            },
        )
        self.assertEqual(self.view.post(self.view.request).status_code, 302)
        self.assertEqual(Bot.objects.count(), 0)
        uuid.uuid1(random.randint(0, 2 ** 48 - 1))
        self.view.bot_id = uuid.uuid1(random.randint(0, 2 ** 48 - 1))
        self.assertEqual(
            self.view.get_success_url(),
            reverse_lazy("game:edit-bot", args=[self.view.bot_id]),
        )
        self.view.request.POST = {
            "create_bot_form-name": "bot_name",
            "create_bot_form-code": Bot.objects.get_default_code,
            "create_bot_form": "create_bot",
        }
        self.assertEqual(self.view.post(self.view.request).status_code, 302)
        self.assertEqual(Bot.objects.count(), 1)
        logout(self.view.request)
        self.assertEqual(self.view.get(self.view.request).status_code, 302)

        try:
            os.remove(f"storage/bot/{self.view.bot_id}.py")
        except FileNotFoundError:
            print(f"Le fichier storage/bot/{self.view.bot_id}.py n'a pas été trouvé.")
