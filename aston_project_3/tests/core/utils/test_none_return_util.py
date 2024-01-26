"""The tests for the none return function."""
from django.test import TransactionTestCase

from apps.core.utils.none_return_util import return_none


class TestNoneReturnUtil(TransactionTestCase):
    """The tests for the none return function."""

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertIsNone(return_none(0))
