"""The tests for the bot match templatetag."""
from django.test import TransactionTestCase

from apps.account.models import User
from apps.game.models import Bot, Match
from apps.game.templatetags.bot_match_templatetag import opponent, issue, score_change


class TestTopicSectionModel(TransactionTestCase):
    """The tests for the bot match templatetag."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        user = User.objects.create_superuser(
            "bot_match_templatetag@test.com", "123456"
        )
        self.bot_left = Bot.objects.create(
            user=user,
            name="bot_left",
            posted=False,
            score=0,
        )
        self.bot_right = Bot.objects.create(
            user=user,
            name="bot_right",
            posted=False,
            score=0,
        )
        self.match = Match.objects.create(
            bot_left=self.bot_left,
            bot_right=self.bot_right,
            movements="",
            result=True,
            score_change_left=-1,
            score_change_right=1,
            output_left=[],
            output_right=[],
            error_messages_left=[],
            error_messages_right=[],
        )
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(opponent(self.match, self.bot_left), self.bot_right)
        self.assertTrue(issue(self.match, self.bot_left))
        self.assertEqual(score_change(self.match, self.bot_left), 1)
