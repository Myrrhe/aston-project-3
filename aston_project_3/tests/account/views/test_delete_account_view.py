"""The tests for the account deletion view"""
from django.http import HttpRequest
from django.test import TransactionTestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from apps.account.models import User
from apps.account.views import DeleteAccountViewSet


class TestDeleteAccountView(TransactionTestCase):
    """The tests for the account deletion view"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.view = DeleteAccountViewSet()
        self.view.request = HttpRequest()
        self.view.request.user = User.objects.create_user(
            "delete_account_view@test.com", "123456"
        )
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(
            self.view.get_form_kwargs(),
            {"initial": {}, "prefix": None, "user": self.view.request.user},
        )
        context_data = self.view.get_context_data()
        self.assertEqual(set(context_data.keys()), {"form", "view", "has_security_key"})
        context_data["form"] = self.view.form_class(
            {"password": "123456"}, user=self.view.request.user
        )
        self.assertTrue(context_data["form"].is_valid())
        self.assertEqual(
            self.view.get_success_url(),
            reverse_lazy("account:account-deleted"),
        )
        self.assertEqual(self.view.form_valid(context_data["form"]).status_code, 302)
        self.assertEqual(User.objects.count(), 0)
