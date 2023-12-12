"""The tests for the login form"""
from django.test import TransactionTestCase

from apps.account.forms import LoginForm


class TestLoginForm(TransactionTestCase):
    """The tests for the login form"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        LoginForm()
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
