"""The bot creation view."""
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView

from apps.core.utils.get_form_util import get_form
from apps.game.forms import CreateBotForm
from apps.game.models import Bot


class CreateBotViewSet(CreateView):
    """The bot creation view."""

    model = Bot
    form_class = CreateBotForm
    template_name = "game/create_bot.html"

    def __init__(self, *args, **kwargs) -> None:
        self.bot_id = ""
        super().__init__(*args, **kwargs)

    def get_success_url(self) -> any:
        """Determine where the user is redirected on success."""
        return reverse_lazy("game:edit-bot", args=[self.bot_id])

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """GET method."""
        if request.user.is_authenticated:
            return render(
                request,
                self.template_name,
                context={
                    "create_bot_form": CreateBotForm(
                        prefix="create_bot_form",
                        user=request.user,
                        initial={
                            "code": "\
import sys\n\
import math\n\
\n\
\n\
# game loop\n\
while True:\n\
    # p: your player number (0 to 1).\n\
    p = int(input())\n\
    for i in range(2):\n\
        # x0: starting X coordinate of lightcycle (or -1)\n\
        # y0: starting Y coordinate of lightcycle (or -1)\n\
        # x1: starting X coordinate of lightcycle (can be the same as X0 if you play before this player)\n\
        # y1: starting Y coordinate of lightcycle (can be the same as Y0 if you play before this player)\n\
        x0, y0, x1, y1 = [int(j) for j in input().split()]\n\
\n\
    # A single line with UP, DOWN, LEFT or RIGHT\n\
    print(\"LEFT\")\n",
                        }
                    ),
                },
            )
        return redirect("account:login", "")

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """POST method."""
        create_bot_form = get_form(
            request, CreateBotForm, "create_bot_form", user=request.user
        )
        if create_bot_form.is_bound and create_bot_form.is_valid():
            # Create bot
            self.bot_id = create_bot_form.save().id
        return redirect(self.get_success_url())

    def get_form_kwargs(self) -> any:
        """Add additionnal kwargs to the form."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
