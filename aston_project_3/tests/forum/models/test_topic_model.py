"""The tests for the topic model"""

from django.core.management import call_command
from django.test import TransactionTestCase

from apps.account.models import User
from apps.core.utils.silence_stdout_util import silence_stdout
from apps.forum.models import Topic, TopicSection


class TestTopicModel(TransactionTestCase):
    """The tests for the topic model"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        User.objects.create_superuser("admin@aston.com", "123456")
        with silence_stdout(django_stdout=True):
            call_command("loaddata", "topic_section_fixtures")
        self.topic_1 = Topic.objects.create(
            title="Titre 1",
            section=TopicSection.objects.first(),
            user=User.objects.first(),
        )
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.topic_1 = Topic.objects.get(title="Titre 1")
        self.assertEqual(self.topic_1.last_activity, self.topic_1.created_at)
        self.assertEqual(self.topic_1.get_replies, -1)
        self.topic_1.increment_view()
        self.assertEqual(self.topic_1.views, 1)
        self.assertEqual(str(self.topic_1), self.topic_1.title)
