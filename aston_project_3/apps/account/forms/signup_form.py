"""The signup form"""
from django import forms

from apps.account.models import User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    """The signup form"""

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
                "id": "email",
            },
        ),
    )

    is_tou_accepted = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={},
        ),
        help_text="J'accepte la Politique de confidentialité et la Politique de cookies. (requis)",
    )

    class Meta(object):
        """The meta class"""

        model = User
        fields = [
            "email",
            "is_tou_accepted",
        ]

    def __init__(self, *args, **kwargs) -> None:
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"placeholder": "Email"})
        self.fields["password1"].widget.attrs.update(
            {
                "placeholder": "Mot de passe",
                "class": "form-control",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "placeholder": "Répétez le mot de passe",
                "class": "form-control",
            }
        )
