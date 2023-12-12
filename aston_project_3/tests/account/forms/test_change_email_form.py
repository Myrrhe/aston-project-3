"""The tests for the mail change form"""
from django.forms import ValidationError
from django.http import HttpRequest
from django.test import TransactionTestCase
from django.utils.translation import gettext_lazy as _

from apps.account.forms import ChangeEmailForm
from apps.account.models import User


class TestChangeEmailForm(TransactionTestCase):
    """The tests for the mail change form"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.new_email = "change_email_form2@test.com"
        self.user = User.objects.create_superuser(
            "change_email_form@test.com", "123456"
        )
        self.form = ChangeEmailForm(
            {"password": "machin", "username": self.new_email},
            user=self.user,
        )
        self.request = HttpRequest()
        self.request.user = self.user
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.form.is_valid()
        with self.assertRaises(ValidationError, msg=_("invalid_credentials")):
            self.form.clean()
        self.form.cleaned_data["password"] = "123456"
        self.assertEqual(
            self.form.clean(),
            {
                "username": self.new_email,
                "password": "123456",
                "security_key": "",
            },
        )
        self.form.save(self.request)
        self.assertEqual(self.user.email, self.new_email)
