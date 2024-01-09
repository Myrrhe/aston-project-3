"""The account deletion form."""
from django import forms

from django.contrib.auth.forms import UsernameField
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django_otp.plugins.otp_totp.models import TOTPDevice

from apps.account.models import User
from apps.core.inputs import NonStickyTextInput


class DeleteAccountForm(forms.Form):
    """The account deletion form."""

    password = UsernameField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("password"),
                "id": "password1",
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

    def delete_account(self) -> None:
        """Delete the account as well as the TOTP associated with it."""
        if self.user.has_security_key():
            TOTPDevice.objects.filter(user_id=self.user.id).delete()
        self.user.delete()

    class Meta(object):
        """The meta class."""

        model = User
        fields = (
            "password",
            "security_key",
        )
