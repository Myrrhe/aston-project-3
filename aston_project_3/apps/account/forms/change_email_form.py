"""The email change form"""
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _

from django import forms

from apps.account.models import User
from apps.core.inputs import NonStickyTextInput
from django.http import HttpRequest


class ChangeEmailForm(forms.Form):
    """The email change form"""

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("email"),
                "id": "email",
            },
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("password"),
                "id": "password",
            },
        ),
    )
    security_key = forms.CharField(
        widget=NonStickyTextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("security_key_optional"),
                "id": "security_key",
                "autocomplete": "off",
            },
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def is_valid(self) -> bool:
        res = True
        res = res and super().is_valid()
        return res

    def save(self, request: HttpRequest) -> None:
        request.user.email = self.cleaned_data["username"]
        request.user.save()

    class Meta(object):
        """The meta class"""

        model = User
        fields = (
            "username",
            "password",
            "security_key",
        )
