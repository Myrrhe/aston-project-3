"""The bot duplication form."""
from django import forms
from werkzeug.utils import secure_filename

from apps.game.models import Bot


class DuplicateBotForm(forms.Form):
    """The bot duplication form."""

    bot_id = forms.UUIDField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            },
        ),
    )

    def __init__(self, *args, **kwargs) -> None:
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str]:
        """Clean the form."""
        return self.cleaned_data

    def duplicate_bot(self) -> Bot:
        """Duplicate the bot."""
        duplicated_bot = Bot.objects.get(id=self.cleaned_data["bot_id"])
        name = duplicated_bot.name + " - Copy"
        index = 1
        while not self.user.is_bot_name_available(name):
            index += 1
            name = duplicated_bot.name + f" - Copy ({index})"
        bot = Bot.objects.create(
            user=self.user,
            name=name,
            posted=False,
            score=0,
        )
        with open("storage/bot/" + secure_filename(f"{bot.id}.py"), "w", newline="", encoding="utf-8") as file:
            file.write(duplicated_bot.get_code)
        return bot

    class Meta(object):
        """The meta class."""

        model = Bot
        fields = (
        )
