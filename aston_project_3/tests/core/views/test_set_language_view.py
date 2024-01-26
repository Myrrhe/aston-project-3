"""The tests for the answer language view"""
from django.test import TransactionTestCase


class TestSetLanguageView(TransactionTestCase):
    """The tests for the language view"""

    def test_standard(self) -> None:
        """Run the tests"""
