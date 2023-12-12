"""The tests for the answer language view"""
from django.test import TransactionTestCase


class TestSetLanguageView(TransactionTestCase):
    """The tests for the language view"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
