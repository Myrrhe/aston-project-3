"""The tests for the signup form"""
from django.test import TransactionTestCase

from apps.account.forms import SignupForm


class TestSignupForm(TransactionTestCase):
    """The tests for the signup form"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        SignupForm()
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
