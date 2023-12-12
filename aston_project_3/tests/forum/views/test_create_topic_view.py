"""The tests for the topic creation view."""
from django.core.management import call_command
from django.http import HttpRequest
from django.test import TransactionTestCase
from django.urls import reverse_lazy

from apps.account.models import User
from apps.forum.models import TopicSection
from apps.forum.views import CreateTopicViewSet


class TestCreateTopicView(TransactionTestCase):
    """The tests for the topic creation view."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        User.objects.create_superuser("admin@aston.com", "123456")
        call_command("loaddata", "topic_section_fixtures")
        self.view = CreateTopicViewSet()
        self.view.request = HttpRequest()
        self.view.request.method = "GET"
        self.view.request.user = User.objects.create_user(
            "create_topic_view@test.com", "123456"
        )
        self.view.object = None
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(
            self.view.get_form_kwargs(),
            {
                "initial": {},
                "prefix": None,
                "instance": None,
                "user": self.view.request.user,
            },
        )
        context_data = self.view.get_context_data()
        self.assertEqual(set(context_data.keys()), {"form", "view"})
        context_data["form"] = self.view.form_class(
            {
                "title": "Titre 1",
                "section": TopicSection.objects.first().code,
                "content": "# Content 1",
            },
            user=self.view.request.user,
        )
        self.assertTrue(context_data["form"].is_valid())
        self.assertEqual(self.view.form_valid(context_data["form"]).status_code, 302)
        self.assertEqual(
            self.view.get_success_url(),
            reverse_lazy("forum:topic", args=[self.view.model.objects.last().id, 1]),
        )
