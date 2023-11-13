"""The security key creation form"""
from base64 import b32encode

from django.utils.translation import gettext_lazy as _

from django import forms
from django.forms import ModelForm, ValidationError
from django_otp.plugins.otp_totp.models import TOTPDevice

from apps.core.inputs import NonStickyTextInput


class CreateSecurityKeyForm(ModelForm):
    """The security key creation form"""

    key = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("key"),
                "id": "key",
            },
        ),
        required=False,
    )
    code = forms.CharField(
        widget=NonStickyTextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("code"),
                "id": "code",
                "autocomplete": "off",
            },
        ),
        required=False,
    )
    key_init = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control d-none",
                "id": "key_init",
                "hidden": "true",
            },
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs) -> None:
        self.request = kwargs.pop("request")
        super(CreateSecurityKeyForm, self).__init__(*args, **kwargs)
        self.fields["key"].initial = b32encode(self.instance.bin_key).decode("utf-8")
        self.fields["key_init"].initial = self.instance.key

    def clean(self) -> dict[str]:
        TOTPDevice.objects.filter(user_id=self.request.user.id).delete()
        self.instance.user_id = self.request.user.id
        self.instance.key = self.cleaned_data["key_init"]
        self.instance.save()
        if not self.instance.verify_token(self.cleaned_data["code"]):
            TOTPDevice.objects.filter(user_id=self.request.user.id).delete()
            raise ValidationError(_("code_did_not_work"))
        return self.cleaned_data

    class Meta(object):
        """The meta class"""

        model = TOTPDevice

        fields = []
