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
        # self.request.path = (
        #     f"/admin/account/user/{self.user.pk}/change/"
        # )
        # self.request.add_form = forms.Form()
        # self.request.user = self.user
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        # self.assertEqual(
        #     get_form(self.request, ChangeEmailForm, "email_form", self.user), ""
        # )
