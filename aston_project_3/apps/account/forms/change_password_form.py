"""The password change form."""
from django.contrib.auth.forms import UsernameField
from django.forms import ValidationError
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from django import forms

from apps.account.models import User
from apps.core.inputs import NonStickyTextInput


class ChangePasswordForm(forms.Form):
    """The password change form."""

    password1 = UsernameField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("current_password"),
                "id": "password1",
            },
        ),
        label=_("current_password"),
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
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("new_password"),
                "id": "password2",
            },
        ),
        label=_("new_password"),
    )
    password3 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("repeat_new_password"),
                "id": "password3",
            },
        ),
        label=_("confirm_new_password"),
    )

    def __init__(self, *args, **kwargs) -> None:
        if "user" in kwargs:
            self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str]:
        """Clean the form."""
        if not self.user.check_credentials(
            self.cleaned_data["password1"],
            self.cleaned_data["security_key"],
        ):
            raise ValidationError(
                _("invalid_credentials"),
                code="invalid_credentials"
            )
        if self.cleaned_data["password2"] != self.cleaned_data["password3"]:
            raise ValidationError(
                _("password_no_match"),
                code="passwords_no_match"
            )
        return self.cleaned_data

    def save(self, request: HttpRequest) -> None:
        """Save the data of the form."""
        request.user.set_password(self.cleaned_data["password2"])
        request.user.save()

    class Meta(object):
        """The meta class."""

        model = User
        fields = (
            "password1",
            "security_key",
            "password2",
            "password3",
        )
