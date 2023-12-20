"""The bot duplication view."""
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import CreateView

from apps.core.utils.get_form_util import get_form
from apps.game.forms import DuplicateBotForm
from apps.game.models import Bot


class DuplicateBotViewSet(CreateView):
    """The bot duplication view."""

    model = Bot
    form_class = DuplicateBotForm

    def get_success_url(self, **kwargs) -> any:
        """Determine where the user is redirected on success."""
        return reverse_lazy("game:edit-bot", args=[self.bot_id])

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """POST method."""
        duplicate_bot_form = get_form(
            request, DuplicateBotForm, "duplicate_bot_form", user=request.user,
        )
        if duplicate_bot_form.is_bound and duplicate_bot_form.is_valid():
            # duplicate bot
            self.bot_id = duplicate_bot_form.duplicate_bot().id
        return redirect(self.get_success_url())

    def get_form_kwargs(self) -> any:
        """Add additionnal kwargs to the form."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
