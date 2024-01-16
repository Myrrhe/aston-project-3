"""The tests for the match model."""
from django.test import TransactionTestCase

from apps.account.models import User
from apps.game.models import Bot, Match


class TestTopicSectionModel(TransactionTestCase):
    """The tests for the match model."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        user = User.objects.create_superuser(
            "match_model@test.com", "123456"
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
        self.bot_bystander = Bot.objects.create(
            user=user,
            name="bot_bystander",
            posted=False,
            score=0,
        )
        self.match = Match(
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
        self.match.save()
        self.assertEqual(Match.objects.get(pk=self.match.id).error_messages_left, [])
        self.assertEqual(Match.objects.get(pk=self.match.id).error_messages_right, [])
        self.match.error_messages_left = [
            ["a"],
            ["b", "c"]
        ]
        self.match.error_messages_right = [
            ["d", "e"],
            ["f"]
        ]
        self.match.save()
        self.assertEqual(Match.objects.get(pk=self.match.id).error_messages_left, [["a", None], ["b", "c"]])
        self.assertEqual(Match.objects.get(pk=self.match.id).error_messages_right, [["d", "e"], ["f", None]])
        self.assertTrue(self.match.am_i_the_bad_guy(self.bot_left))
        self.assertFalse(self.match.am_i_the_bad_guy(self.bot_right))
        with self.assertRaises(ValueError, msg="This bot didn't fought in this match"):
            self.match.am_i_the_bad_guy(self.bot_bystander)
        self.assertEqual(self.match.get_opponent(self.bot_left), self.bot_right)
        self.assertEqual(self.match.get_opponent(self.bot_right), self.bot_left)
        self.assertTrue(self.match.get_result(self.bot_left))
        self.assertFalse(self.match.get_result(self.bot_right))
        self.assertEqual(self.match.get_score_change(self.bot_left), self.match.score_change_right)
        self.assertEqual(self.match.get_score_change(self.bot_right), self.match.score_change_left)
        self.assertEqual(str(self.match), f"{self.bot_left} vs {self.bot_right}")
