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
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str]:
        if self.request.user.check_password(self.cleaned_data["password"]) and (
            not self.request.user.has_security_key()
            or verify_token(
                self.request.user,
                TOTPDevice.objects.get(user_id=self.request.user.id).persistent_id,
                self.cleaned_data["security_key"],
            )
        ):
            return self.cleaned_data
        else:
            raise ValidationError(_("authentication_error"))

    def delete_account(self) -> None:
        print("###########################################################")
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
