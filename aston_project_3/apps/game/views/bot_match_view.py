"""One match of a bot view."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from apps.game.models import Bot, Match


class BotMatchViewSet(View):
    """One match of a bot view."""

    def get(
        self,
        request: HttpRequest,
        bot_id: str,
        match_id: str,
    ) -> HttpResponse:
        """GET method."""
        if request.user.is_authenticated:
            bot = Bot.objects.get(pk=bot_id)
            if bot.user.id != request.user.id:
                return redirect("game:my-bots")
            match = Match.objects.get(pk=match_id)
            if bot_id not in {match.bot_left.id, match.bot_right.id}:
                return redirect("game:bot-matches", bot_id)
            return render(
                request,
                "game/bot_match.html",
                context={
                    "bot": bot,
                    "match": match,
                },
            )
        return redirect("account:login", "")
