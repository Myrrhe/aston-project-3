"""The bot duplication form."""
from django import forms

from apps.game.models import Bot


class TogglePublishBotForm(forms.Form):
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
        if "bot_id" in kwargs:
            self.bot_id = kwargs.pop("bot_id")
        else:
            self.bot_id = None
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str]:
        """Clean the form."""
        return self.cleaned_data

    def toggle_publish(self) -> Bot:
        """Switch the posted status of the bot."""
        bot = Bot.objects.get(pk=self.bot_id)
        bot.posted = not bot.posted
        bot.save()
        return bot

    class Meta(object):
        """The meta class."""

        model = Bot
        fields = (
        )
