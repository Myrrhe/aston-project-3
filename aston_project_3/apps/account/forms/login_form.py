"""The login form"""
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext as _

from django import forms

from apps.account.models import User
from apps.core.inputs import NonStickyTextInput


class LoginForm(AuthenticationForm):
    """The login form"""

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
                "placeholder": _("security_key_optionnal"),
                "id": "security_key",
                "autocomplete": "off",
            },
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs) -> None:
        super(LoginForm, self).__init__(*args, **kwargs)

    class Meta(object):
        """The meta class"""

        model = User
        fields = (
            "username",
            "password",
            "security_key",
        )
