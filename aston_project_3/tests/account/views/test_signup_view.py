"""The tests for the signup view."""
from django.test import TransactionTestCase
from django.urls import reverse_lazy

from apps.account.views import SignupViewSet


class TestSignupView(TransactionTestCase):
    """The tests for the non sticky text input."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.view = SignupViewSet()
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(
            self.view.get_success_url(), reverse_lazy("account:account-created")
        )
