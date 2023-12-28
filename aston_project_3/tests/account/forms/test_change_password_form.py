"""The tests for the password change form"""
from django.forms import ValidationError
from django.http import HttpRequest
from django.test import TransactionTestCase
from django.utils.translation import gettext_lazy as _

from apps.account.forms import ChangePasswordForm
from apps.account.models import User


class TestChangePasswordForm(TransactionTestCase):
    """The tests for the password change form"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.user = User.objects.create_user(
            "change_password_form_1@test.com", password="123456"
        )
        self.form1 = ChangePasswordForm(
            {"password1": "truc", "password2": "machin", "password3": "machin"}
        )
        self.form1 = ChangePasswordForm(
            {"password1": "truc", "password2": "machin", "password3": "bidule"},
            user=self.user,
        )
        self.old_password = self.user.password
        self.request = HttpRequest()
        self.request.user = self.user
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.form1.is_valid()
        with self.assertRaises(ValidationError, msg=_("invalid_credentials")):
            self.form1.clean()
        self.form1.cleaned_data["password1"] = "123456"
        with self.assertRaises(ValidationError, msg=_("password_no_match")):
            self.form1.clean()
        self.form1.cleaned_data["password2"] = "bidule"
        self.assertEqual(
            self.form1.clean(),
            {
                "password1": "123456",
                "password2": "bidule",
                "password3": "bidule",
                "security_key": "",
            },
        )
        self.form1.save(self.request)
        self.assertNotEqual(self.user.password, self.old_password)
