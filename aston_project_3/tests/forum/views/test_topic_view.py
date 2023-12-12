"""The tests for the topic view."""
from django.test import TransactionTestCase


class TestTopicView(TransactionTestCase):
    """The tests for the topic view."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
