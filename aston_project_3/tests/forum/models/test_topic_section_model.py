"""The tests for the topic section model"""
from django.core.management import call_command
from django.test import TransactionTestCase

from apps.account.models import User
from apps.forum.models import TopicSection


class TestTopicSectionModel(TransactionTestCase):
    """The tests for the topic section model"""

    fixtures = ["topic_section_fixtures"]

    def setUp(self) -> None:
        """Set up the data for the tests"""
        User.objects.create_superuser("admin@aston.com", "123456")
        call_command("loaddata", "topic_section_fixtures")
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        topic_section_bug = TopicSection.objects.get(code="bug")
        self.assertEqual(set(TopicSection.get_all()), {("bot", "Bot programming"), ("bug", "Feedback & Bugs")})
        self.assertEqual(topic_section_bug.natural_key(), (topic_section_bug.code,))
        self.assertEqual(
            str(topic_section_bug),
            f"{topic_section_bug.name} ({topic_section_bug.code})",
        )
