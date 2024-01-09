"""The bot deletion view."""
from django.forms import Form
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from apps.account.models import User
from apps.game.forms import DeleteBotForm


class DeleteBotViewSet(FormView):
    """The bot deletion view."""

    model = User
    form_class = DeleteBotForm
    template_name = "game/delete_bot.html"

    def get_success_url(self) -> any:
        """Determine where the user is redirected on success."""
        return reverse_lazy(
            "game:bot-deleted",
        )

    def get(
        self,
        request: HttpRequest,
        bot_id: str,
    ) -> HttpResponse:
        """GET method."""
        return render(
            request,
            self.template_name,
            context={
                "bot_id": bot_id,
            },
        )

    def form_valid(self, form: Form) -> HttpResponse:
        """Trigger an action when the submitted form is valid."""
        form.delete_bot()
        return super().form_valid(form)

    def get_form_kwargs(self) -> any:
        """
        Pass the request object to the form class.

        This is necessary to give the current user to the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
