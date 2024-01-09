"""The signup form."""
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _

from apps.account.models import User


class SignupForm(UserCreationForm):
    """The signup form."""

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("email"),
                "id": "email",
            },
        ),
    )

    is_tou_accepted = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={},
        ),
        help_text=_("tou_text"),
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"placeholder": "Email"})
        self.fields["password1"].widget.attrs.update(
            {
                "placeholder": _("password"),
                "class": "form-control",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "placeholder": _("password_repeat"),
                "class": "form-control",
            }
        )

    class Meta(object):
        """The meta class."""

        model = User
        fields = [
            "email",
            "is_tou_accepted",
        ]
