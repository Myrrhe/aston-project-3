"""The toggle for the publication of the bot view."""
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView

from apps.core.utils.get_form_util import get_form
from apps.game.forms import TogglePublishBotForm
from apps.game.models import Bot


class TogglePublishBotViewSet(UpdateView):
    """The toggle for the publication of the bot view."""

    model = Bot
    form_class = TogglePublishBotForm

    def get_success_url(self, **kwargs) -> any:
        """Determine where the user is redirected on success."""
        return reverse_lazy("game:edit-bot", args=[self.bot_id])

    def post(self, request: HttpRequest, bot_id: str, *args, **kwargs) -> JsonResponse:
        """POST method."""
        toggle_publish_bot_form = get_form(
            request,
            TogglePublishBotForm,
            "toggle_publish_bot_form",
            user=request.user,
            bot_id=bot_id,
        )
        if toggle_publish_bot_form.is_bound and toggle_publish_bot_form.is_valid():
            # Toggle publish bot
            bot = toggle_publish_bot_form.toggle_publish()
            self.bot_id = bot.id
        # return redirect(self.get_success_url())
        return JsonResponse({
            "message": "Posted status changed",
            "posted": bot.posted,
        }, status="200", content_type="text/json")

    def get_form_kwargs(self) -> any:
        """Add additionnal kwargs to the form."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
