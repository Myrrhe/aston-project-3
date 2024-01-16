"""Allow to get a match from a bot point of view."""
from django import template

from apps.game.models import Bot, Match

register = template.Library()


@register.filter(name="opponent")
def opponent(match: Match, bot: Bot) -> Bot:
    """Get the opponent in a match."""
    return match.getOpponent(bot)

@register.filter(name="issue")
def issue(match: Match, bot: Bot) -> bool:
    """Get the issue in a match."""
    return match.getResult(bot)

@register.filter(name="score_change")
def score_change(match: Match, bot: Bot) -> int:
    """Get the issue in a match."""
    return match.getScoreChange(bot)
