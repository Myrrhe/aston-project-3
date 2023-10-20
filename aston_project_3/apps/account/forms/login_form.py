"""The login form"""
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from django import forms

from apps.account.models import User


class LoginForm(AuthenticationForm):
    """The login form"""

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
                "id": "email",
            },
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Mot de passe",
                "id": "password",
            },
        ),
    )
    security_key = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Clef de sécurité (optionel)",
                "id": "security_key",
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