"""The bot deletion form."""
from django import forms
import os
from werkzeug.utils import secure_filename

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
        if os.path.exists("storage/bot/" + secure_filename(f"{self.cleaned_data['bot_id']}.py")):
            os.remove("storage/bot/" + secure_filename(f"{self.cleaned_data['bot_id']}.py"))
        Bot.objects.get(id=self.cleaned_data["bot_id"]).delete()

    class Meta(object):
        """The meta class."""

        model = Bot
        fields = (
        )
