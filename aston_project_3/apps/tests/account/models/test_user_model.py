"""The tests for the user model"""
import sys

from django.test import TransactionTestCase

from apps.account.models import User


class TestUserModel(TransactionTestCase):
    """The tests for the user model"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        print("machin", file=sys.stderr)
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        print("truc", file=sys.stderr)
        self.assertEqual(self.answer.__str__(), "I am : 18-28 years old")
