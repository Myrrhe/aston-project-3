"""The tests for the topic creation form"""
from django.core.management import call_command
from django.http import HttpRequest
from django.test import TransactionTestCase

from apps.account.models import User
from apps.core.utils.silence_stdout_util import silence_stdout
from apps.forum.forms import CreateTopicForm
from apps.forum.models import Post, Topic


class TestCreateTopicForm(TransactionTestCase):
    """The tests for the topic creation form"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.user = User.objects.create_superuser(
            "create_topic_form@test.com", "123456"
        )
        User.objects.create_superuser("admin@aston.com", "123456")
        with silence_stdout(django_stdout=True):
            call_command("loaddata", "topic_section_fixtures")
        self.request = HttpRequest()
        self.request.user = self.user
        self.form = CreateTopicForm(
            {"section": "bug", "title": "Premier topic", "content": "# Bonjour !"},
            user=self.user,
        )
        self.form.is_valid()
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.form.save(commit=False)
        self.assertEqual(Topic.objects.count(), 0)
        self.assertEqual(Post.objects.count(), 0)
        self.form.save()
        self.assertEqual(Topic.objects.count(), 1)
        self.assertEqual(Post.objects.count(), 1)
