"""The tests for the account deletion form"""
from django.forms import ValidationError
from django.test import TransactionTestCase
from django.utils.translation import gettext_lazy as _
from django_otp.plugins.otp_totp.models import TOTPDevice

from apps.account.forms import DeleteAccountForm
from apps.account.models import User


class TestDeleteAccountForm(TransactionTestCase):
    """The tests for the account deletion form"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.user = User.objects.create_user(
            "delete_account_form_1@test.com", password="123456"
        )
        self.superuser = User.objects.create_superuser(
            "delete_account_form_2@test.com", password="123456"
        )
        TOTPDevice.objects.create(
            name="admin_key",
            user_id=self.superuser.id,
        )
        self.form1 = DeleteAccountForm({"password": "machin"}, user=self.user)
        self.form2 = DeleteAccountForm(
            {"password": "123456", "security_key": "123456"}, user=self.superuser
        )
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.form1.is_valid()
        self.form2.is_valid()
        with self.assertRaises(ValidationError, msg=_("invalid_credentials")):
            self.form1.clean()
        self.form1.cleaned_data["password"] = "123456"
        self.assertEqual(self.form1.clean(), {"password": "123456", "security_key": ""})
        self.form1.delete_account()
        self.assertEqual(User.objects.count(), 1)
        self.form2.delete_account()
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(TOTPDevice.objects.count(), 0)
