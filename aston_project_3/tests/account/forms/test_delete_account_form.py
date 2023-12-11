"""The tests for the login form"""
from django.forms import ValidationError
from django.test import TransactionTestCase
from django.utils.translation import gettext_lazy as _

from apps.account.forms import DeleteAccountForm
from apps.account.models import User


class TestDeleteAccountForm(TransactionTestCase):
    """The tests for the login form"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.user = User.objects.create_user(
            "delete_account_form_1@test.com", password="123456"
        )
        self.form = DeleteAccountForm({"password": "machin"}, user=self.user)
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.form.is_valid()
        with self.assertRaises(ValidationError, msg=_("invalid_credentials")):
            self.form.clean()
        self.form.cleaned_data["password"] = "123456"
        self.assertEqual(self.form.clean(), {"password": "123456", "security_key": ""})
        self.form.delete_account()
        self.assertEqual(User.objects.count(), 0)
