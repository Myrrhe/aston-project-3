"""The tests for the CSRF getter view."""
from django.http import HttpRequest
from django.test import TransactionTestCase

from apps.core.views import GetCSRFViewSet


class TestGetCsrfView(TransactionTestCase):
    """The tests for the CSRF getter view."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.request = HttpRequest()
        self.view = GetCSRFViewSet()
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(self.view.get(self.request).status_code, 200)
