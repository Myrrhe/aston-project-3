"""The personnal informations change form"""
from django.utils.translation import gettext_lazy as _

from django import forms

from apps.account.models import User
from django.http import HttpRequest


class PersonalInformationsForm(forms.Form):
    """The personnal informations change form."""

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("pseudo"),
                "id": "pseudo",
            },
        ),
        label=_("pseudo"),
    )
    biography = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("biography"),
                "id": "biography",
            },
        ),
        label=_("biography"),
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def save(self, request: HttpRequest) -> None:
        """Save the data of the form."""
        request.user.username = self.cleaned_data["username"]
        request.user.biography = self.cleaned_data["biography"]
        request.user.save()

    class Meta(object):
        """The meta class."""

        model = User
        fields = (
            "username",
            "biography",
        )
