"""The tests for the answer topic form"""
from django.core.management import call_command
from django.http import HttpRequest
from django.test import TransactionTestCase

from apps.account.models import User
from apps.core.utils.silence_stdout_util import silence_stdout
from apps.forum.forms import AnswerTopicForm
from apps.forum.models import Post, Topic, TopicSection


class TestAnswerTopicForm(TransactionTestCase):
    """The tests for the answer topic form"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.user = User.objects.create_superuser(
            "answer_topic_form@test.com", "123456"
        )
        User.objects.create_superuser("admin@aston.com", "123456")
        with silence_stdout(django_stdout=True):
            call_command("loaddata", "topic_section_fixtures")
        self.request = HttpRequest()
        self.request.user = self.user
        self.topic_1 = Topic.objects.create(
            title="Titre 1",
            section=TopicSection.objects.first(),
            user=self.user,
        )
        self.form = AnswerTopicForm(
            {"topic_id": self.topic_1.id, "content": "# Bonjour !"}
        )
        self.form.is_valid()
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(
            self.form.clean(), {"topic_id": self.topic_1.id, "content": "# Bonjour !"}
        )
        self.form.save(self.request)
        self.assertEqual(Post.objects.count(), 1)
