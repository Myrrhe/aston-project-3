"""The bot edition view."""
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView

from apps.core.utils.get_form_util import get_form
from apps.game.forms import CreateBotForm
from apps.game.models import Bot


class EditBotViewSet(UpdateView):
    """The bot edition view."""

    model = Bot
    form_class = CreateBotForm
    template_name = "game/create_bot.html"

    def get_success_url(self, **kwargs) -> any:
        """Determine where the user is redirected on success."""
        return reverse_lazy("game:edit-bot", args=[self.bot_id])

    def get(
        self,
        request: HttpRequest,
        bot_id: str,
        *args,
        **kwargs
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
                "create_bot_form": CreateBotForm(
                    prefix="create_bot_form",
                    user=request.user,
                    bot_id=bot_id,
                    initial={
                        "name": bot.name,
                        "code": code,
                    }
                ),
            },
        )

    def post(self, request: HttpRequest, bot_id: str, *args, **kwargs) -> HttpResponse:
        """POST method."""
        create_bot_form = get_form(
            request, CreateBotForm, "create_bot_form", user=request.user, bot_id=bot_id,
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
