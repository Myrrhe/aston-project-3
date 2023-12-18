"""The bot deletion form."""
from django.utils.translation import gettext_lazy as _

from django import forms

from apps.game.models import Bot


class DeleteBotForm(forms.Form):
    """The bot deletion form."""

    bot_id = forms.UUIDField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control d-none",
                "id": "bot",
            },
        ),
    )

    def __init__(self, *args, **kwargs) -> None:
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str]:
        """Clean the form."""
        return self.cleaned_data

    def delete_bot(self) -> None:
        """Delete the bot."""
        Bot.objects.get(id=self.cleaned_data["bot_id"]).delete()

    class Meta(object):
        """The meta class."""

        model = Bot
        fields = (
        )
