"""The tests for the account deleted view."""
from django.http import HttpRequest
from django.test import TransactionTestCase

from apps.account.views import AccountDeletedViewSet


class TestAccountDeletedView(TransactionTestCase):
    """The tests for the account deleted view."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.request = HttpRequest()
        self.request.method = "GET"
        self.view = AccountDeletedViewSet()
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(self.view.get(self.request).status_code, 200)
