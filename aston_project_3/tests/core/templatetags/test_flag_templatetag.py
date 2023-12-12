"""The tests for the flag templatetag"""
from django.test import TransactionTestCase

from apps.core.templatetags.flag_templatetag import flag


class TestFlagTemplatetag(TransactionTestCase):
    """The tests for the flag templatetag"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(flag(""), "")
        self.assertEqual(flag("fr"), "🇫🇷")
        self.assertEqual(flag("en"), "🇬🇧")
