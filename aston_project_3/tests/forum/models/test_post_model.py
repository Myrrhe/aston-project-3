"""The tests for the post model"""

from django.core.management import call_command
from django.test import TransactionTestCase

from apps.account.models import User
from apps.core.utils.silence_stdout_util import silence_stdout
from apps.forum.models import Post
from apps.forum.models import Topic
from apps.forum.models import TopicSection


class TestPostModel(TransactionTestCase):
    """The tests for the post model"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        user = User.objects.create_superuser("post_model@test.com", "123456")
        with silence_stdout(django_stdout=True):
            call_command("loaddata", "topic_section_fixtures")
        Topic.objects.create(
            title="Titre 1",
            section=TopicSection.objects.first(),
            user=user,
        )
        self.post_1 = Post.objects.create(
            content="# Post 1",
            topic=Topic.objects.first(),
            user=user,
        )
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(self.post_1.get_text_html, "<h1>Post 1</h1>\n")
        self.assertEqual(
            str(self.post_1), f"{self.post_1.topic.title} : {self.post_1.user}"
        )
