"""The tests for the topic section model"""

from django.test import TransactionTestCase

from apps.forum.models import TopicSection


class TestTopicSectionModel(TransactionTestCase):
    """The tests for the topic section model"""

    fixtures = ["topic_section_fixtures"]

    def setUp(self) -> None:
        """Set up the data for the tests"""
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        topic_section_bug = TopicSection.objects.get(code="bug")
        self.assertEqual(topic_section_bug.natural_key(), (topic_section_bug.code,))
        self.assertEqual(
            str(topic_section_bug),
            f"{topic_section_bug.name} ({topic_section_bug.code})",
        )
