"""The email change form."""
from django.contrib.auth.forms import UsernameField
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest

from django import forms

from apps.account.models import User
from apps.core.inputs import NonStickyTextInput


class ChangeEmailForm(forms.Form):
    """The email change form."""

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("email"),
                "id": "email",
            },
        ),
        label=_("new_email"),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("password"),
                "id": "password",
            },
        ),
        label=_("password"),
    )
    security_key = forms.CharField(
        widget=NonStickyTextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("security_key"),
                "id": "security_key",
                "autocomplete": "off",
            },
        ),
        required=False,
        label=_("security_key"),
    )

    def __init__(self, *args, **kwargs) -> None:
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str]:
        """Clean the form."""
        if not self.user.check_credentials(
            self.cleaned_data["password"],
            self.cleaned_data["security_key"],
        ):
            raise ValidationError(
                _("invalid_credentials"),
                code="invalid_credentials"
            )
        return self.cleaned_data

    def save(self, request: HttpRequest) -> None:
        """Save the data of the form."""
        request.user.email = self.cleaned_data["username"]
        request.user.save()

    class Meta(object):
        """The meta class."""

        model = User
        fields = (
            "username",
            "password",
            "security_key",
        )
