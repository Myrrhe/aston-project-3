"""The tests for the forum view."""
from django.core.management import call_command
from django.http import HttpRequest
from django.test import TransactionTestCase

from apps.account.models import User
from apps.forum.views import ForumViewSet


class TestForumView(TransactionTestCase):
    """The tests for the forum view."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        User.objects.create_superuser("admin@aston.com", "123456")
        call_command("loaddata", "topic_section_fixtures")
        self.view = ForumViewSet()
        self.request = HttpRequest()
        self.request.method = "GET"
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(self.view.get(self.request, "all", "new", 0).status_code, 200)
        self.assertEqual(self.view.get(self.request, "bug", "old", 1).status_code, 200)
        self.assertEqual(self.view.get(self.request, "all", "new", 2).status_code, 200)
        self.assertEqual(
            self.view.get(self.request, "all", "machin", 1).status_code, 302
        )
