"""The starting view."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from apps.game.models import Bot, Match


class StartViewSet(View):
    """The starting view."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """GET method."""
        if not Match.objects.exists():
            return render(request, "home/start.html")
        match = Match.objects.order_by("?").first()
        return render(
            request,
            "home/start.html",
            context={
                "match": match,
                "bot": match.bot_left,
            }
        )
