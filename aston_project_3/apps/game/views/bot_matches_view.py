"""The matches by bot view."""
from itertools import chain

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from apps.game.models import Bot


class BotMatchesViewSet(View):
    """The matches by bot view."""

    def get(
        self,
        request: HttpRequest,
        bot_id: str,
    ) -> HttpResponse:
        """GET method."""
        if request.user.is_authenticated:
            bot = Bot.objects.get(pk=bot_id)
            if bot.user.id != request.user.id:
                return redirect("game:my-bots")
            matches = list(chain(bot.matches_as_left.all(), bot.matches_as_right.all()))
            return render(
                request,
                "game/bot_matches.html",
                context={
                    "bot": bot,
                    "matches": matches,
                },
            )
        return redirect("account:login", "")
