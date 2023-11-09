"""The password change form"""
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _

from django import forms

from apps.account.models import User
from apps.core.inputs import NonStickyTextInput
from django.http import HttpRequest


class ChangePasswordForm(forms.Form):
    """The password change form"""

    password1 = UsernameField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("current_password"),
                "id": "password1",
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
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("new_password"),
                "id": "password2",
            },
        ),
    )
    password3 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("repeat_new_password"),
                "id": "password3",
            },
        ),
    )

    def __init__(self, *args, **kwargs) -> None:
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def is_valid(self) -> bool:
        res = True
        res = res and super(ChangePasswordForm, self).is_valid()
        return res

    def save(self, request: HttpRequest) -> None:
        request.user.set_password(self.cleaned_data["password2"])
        request.user.save()

    class Meta(object):
        """The meta class"""

        model = User
        fields = (
            "password1",
            "security_key",
            "password2",
            "password3",
        )
