"""The tests for the timer."""
import time

from django.test import TransactionTestCase

from apps.core.utils import RepeatedTimer


class TestRepeatedTimer(TransactionTestCase):
    """The tests for the timer."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.repeated_timer = RepeatedTimer(1, lambda: True)
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertTrue(self.repeated_timer.is_running)
        time.sleep(2)
        self.repeated_timer.start()
        self.repeated_timer.stop()
        self.assertFalse(self.repeated_timer.is_running)
