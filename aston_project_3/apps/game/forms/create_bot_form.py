"""The bot creation form."""
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms
from djangocodemirror.fields import CodeMirrorField
from djangocodemirror.widgets import CodeMirrorWidget
from werkzeug.utils import secure_filename

from apps.game.models import Bot


class CreateBotForm(ModelForm):
    """The bot creation form."""

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-1",
                "placeholder": _("bot_name"),
                "id": "name",
            },
        ),
        label=_("name"),
    )

    code = CodeMirrorField(
        config_name="python",
        widget=CodeMirrorWidget(
            attrs={}
        ),
        label=_("code"),
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

    def save(self) -> Bot:
        """Save the data of the form."""
        bot = None
        if self.bot_id:
            bot = Bot.objects.get(pk=self.bot_id)
            bot.name = self.cleaned_data["name"]
            bot.save()
        else:
            bot = Bot.objects.create(
                user=self.user,
                name=self.cleaned_data["name"],
                posted=False,
                score=0,
            )
        with open("storage/bot/" + secure_filename(f"{bot.id}.py"), "w", newline="", encoding="utf-8") as file:
            file.write(self.cleaned_data["code"])
        return bot

    class Meta(object):
        """The meta class."""

        model = Bot
        fields = (
            "name",
        )
