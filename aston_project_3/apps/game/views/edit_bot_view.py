"""The bot edition view."""
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView

from apps.core.utils.get_form_util import get_form
from apps.game.forms import CreateBotForm, DuplicateBotForm, TogglePublishBotForm
from apps.game.models import Bot, Match


class EditBotViewSet(UpdateView):
    """The bot edition view."""

    model = Bot
    form_class = CreateBotForm
    template_name = "game/create_bot.html"

    def __init__(self, *args, **kwargs) -> None:
        self.bot_id = ""
        super().__init__(*args, **kwargs)

    def get_success_url(self) -> any:
        """Determine where the user is redirected on success."""
        return reverse_lazy("game:edit-bot", args=[self.bot_id])

    def get(
        self,
        request: HttpRequest,
        bot_id: str,
    ) -> HttpResponse:
        """GET method."""
        if not request.user.is_authenticated:
            return redirect("account:login", "")
        bot = Bot.objects.get(pk=bot_id)
        if bot.user.id != request.user.id:
            return redirect("game:my-bots")
        code = bot.get_code
        return render(
            request,
            self.template_name,
            context={
                "bot_id": bot_id,
                "posted": bot.posted,
                "create_bot_form": CreateBotForm(
                    prefix="create_bot_form",
                    user=request.user,
                    bot_id=bot_id,
                    initial={
                        "name": bot.name,
                        "code": code,
                    }
                ),
                "duplicate_bot_form": DuplicateBotForm(
                    prefix="duplicate_bot_form",
                    user=request.user,
                    initial={
                        "bot_id": bot_id,
                    }
                ),
                "toggle_publish_bot_form": TogglePublishBotForm(
                    prefix="toggle_publish_bot_form",
                    user=request.user,
                    bot_id=bot_id,
                    initial={
                        "bot_id": bot_id,
                    }
                ),
            },
        )

    def post(self, request: HttpRequest, bot_id: str) -> JsonResponse:
        """POST method."""
        create_bot_form = get_form(
            request, CreateBotForm, "create_bot_form", user=request.user, bot_id=bot_id,
        )
        match = None
        if create_bot_form.is_bound and create_bot_form.is_valid():
            # Create bot
            bot = create_bot_form.save()
            self.bot_id = bot.id
            opponent_bot = Bot.objects.get_by_natural_key("admin@aston.com", "Bot 1")
            match = Match.objects.bot_fight(bot, opponent_bot)
        else:
            self.bot_id = bot_id
        return JsonResponse({
            "message": "Bot saved",
            "bot_name": bot.name,
            "match_movements": match.movements if match else "",
            "match_result": match.result if match else "",
            "match_even": match.bot_left.id == bot.id if match else "",
        }, status="200", content_type="text/json")

    def get_form_kwargs(self) -> any:
        """Add additionnal kwargs to the form."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
