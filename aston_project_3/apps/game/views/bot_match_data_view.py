"""Data of a match of a bot view."""
from django.http import HttpRequest, JsonResponse
from django.utils.html import escape
from django.views import View

from apps.game.models import Bot, Match


class BotMatchDataViewSet(View):
    """Data of a match of a bot view."""

    def get(
        self,
        request: HttpRequest,
        bot_id: str,
        match_id: str,
    ) -> JsonResponse:
        """GET method."""
        if request.user.is_authenticated:
            bot = Bot.objects.get(pk=bot_id)
            if bot.user.id != request.user.id:
                return JsonResponse({}, status="403", content_type="text/json")
            match = Match.objects.get(pk=match_id)
            if match.bot_left.id != bot_id and match.bot_right.id != bot_id:
                return JsonResponse({}, status="403", content_type="text/json")
            return JsonResponse({
                "bot_name": escape(bot.name),
                "match_movements": match.movements if match else "",
                "stdout": [match.output_left, match.output_right],
                "stderr": [match.error_messages_left, match.error_messages_right],
                "match_result": match.result if match else "",
                "match_even": match.bot_left.id == bot.id if match else "",
            }, status="200", content_type="text/json")
        else:
            return JsonResponse({}, status="403", content_type="text/json")
