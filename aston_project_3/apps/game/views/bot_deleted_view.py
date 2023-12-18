"""The bot deleted view."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class BotDeletedViewSet(View):
    """The bot deleted view."""

    template_name = "game/bot_deleted.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """GET method."""
        return render(request, self.template_name)
