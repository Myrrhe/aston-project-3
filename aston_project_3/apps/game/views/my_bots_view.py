"""The personnal bots view."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from apps.game.models import Bot


class MyBotsViewSet(View):
    """The personnal bots view."""

    def get(
        self,
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> HttpResponse:
        """GET method."""
        if request.user.is_authenticated:
            bots = Bot.objects.filter(user=request.user)
            return render(
            request,
            "game/my_bots.html",
            context={
                "bots": bots,
            },
        )
        else:
            return redirect("account:login", "")
