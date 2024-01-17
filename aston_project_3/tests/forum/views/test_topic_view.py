"""The tests for the topic view."""
from django.core.management import call_command
from django.http import HttpRequest
from django.test import TransactionTestCase

from apps.account.models import User
from apps.core.utils.silence_stdout_util import silence_stdout
from apps.forum.models import Topic, TopicSection
from apps.forum.views import TopicViewSet


class TestTopicView(TransactionTestCase):
    """The tests for the topic view."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        User.objects.create_superuser("admin@aston.com", "123456")
        with silence_stdout(django_stdout=True):
            call_command("loaddata", "topic_section_fixtures")
        user = User.objects.create_user("topic_view@test.com", "123456")
        self.topic_1_id = Topic.objects.create(
            title="Titre 1",
            section=TopicSection.objects.first(),
            user=user,
        ).id
        self.view = TopicViewSet()
        self.request = HttpRequest()
        self.request.method = "GET"
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(
            self.view.get(self.request, self.topic_1_id, -1).status_code, 200
        )
        self.assertEqual(
            self.view.get(self.request, self.topic_1_id, 0).status_code, 200
        )
        self.assertEqual(
            self.view.get(self.request, self.topic_1_id, 1).status_code, 200
        )
