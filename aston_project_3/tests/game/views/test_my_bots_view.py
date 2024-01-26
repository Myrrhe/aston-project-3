"""The tests for my bots view."""
from importlib import import_module

from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpRequest
from django.test import TransactionTestCase, Client

from apps.account.models import User
from apps.game.views import MyBotsViewSet


class TestMyBotsView(TransactionTestCase):
    """The tests for my bots view."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.client = Client()
        self.request = HttpRequest()
        self.request.method = "GET"
        self.request.path = "/fr-fr/login/"
        self.request.session = None
        self.request.user = User.objects.create_user(
            "my_bots_view@test.com", "123456"
        )

        engine = import_module(settings.SESSION_ENGINE)
        self.request.session = engine.SessionStore()

        self.view = MyBotsViewSet()
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(self.view.get(self.request).status_code, 200)
        logout(self.request)
        self.assertEqual(self.view.get(self.request).status_code, 302)
