"""The tests for the form getter"""
from django.http import HttpRequest
from django.test import TransactionTestCase

from apps.account.forms import ChangeEmailForm
from apps.account.models import User
from apps.core.utils.get_form_util import get_form


class TestGetForm(TransactionTestCase):
    """The tests for the form getter"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.user = User.objects.create_superuser("get_form@test.com", "123456")
        self.request = HttpRequest()
        self.request.method = "GET"
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(
            type(get_form(self.request, ChangeEmailForm, "email_form", user=self.user)),
            ChangeEmailForm,
        )
