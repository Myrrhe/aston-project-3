"""The account deletion form"""
from django.contrib.auth.forms import UsernameField
from django.forms import ValidationError
from django_otp import verify_token
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.utils.translation import gettext_lazy as _

from django import forms

from apps.account.models import User
from apps.core.inputs import NonStickyTextInput


class DeleteAccountForm(forms.Form):
    """The account deletion form"""

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
        if not self.user.check_credentials(
            self.cleaned_data["password"],
            self.cleaned_data["security_key"],
        ):
            raise ValidationError(_("invalid_credentials"), code="invalid_credentials")
        return self.cleaned_data

    def delete_account(self) -> None:
        if self.request.user.has_security_key():
            TOTPDevice.objects.filter(user_id=self.request.user.id).delete()
        self.request.user.delete()

    class Meta(object):
        """The meta class"""

        model = User
        fields = (
            "password",
            "security_key",
        )
