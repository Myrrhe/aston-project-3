"""The tests for the topic creation view."""
from django.core.management import call_command
from django.http import HttpRequest
from django.test import TransactionTestCase

from apps.account.models import User
from apps.forum.models import Post, Topic, TopicSection
from apps.forum.views import AnswerTopicViewSet


class TestAnswerTopicView(TransactionTestCase):
    """The tests for the topic creation view."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        User.objects.create_superuser("admin@aston.com", "123456")
        call_command("loaddata", "topic_section_fixtures")
        self.view = AnswerTopicViewSet()
        self.request = HttpRequest()
        self.request.method = "POST"
        self.request.user = User.objects.create_user(
            "create_topic_view@test.com", "123456"
        )
        self.view.object = None
        self.topic_1 = Topic.objects.create(
            title="Titre 1",
            section=TopicSection.objects.first(),
            user=self.request.user,
        )
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(self.view.post(self.request).status_code, 302)
        self.assertEqual(Post.objects.count(), 0)
        self.request.POST = {"content": "# Bonjour !", "topic_id": self.topic_1.id}
        self.assertEqual(self.view.post(self.request).status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
