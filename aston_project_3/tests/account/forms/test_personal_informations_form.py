"""The tests for the personal informations form"""
from django.core.management import call_command
from django.http import HttpRequest
from django.test import TransactionTestCase

from apps.account.models import User
from apps.account.forms import PersonalInformationsForm


class TestPersonalInformationsForm(TransactionTestCase):
    """The tests for the personal informations form"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.user = User.objects.create_superuser(
            "personal_informations_form@test.com", "123456"
        )
        self.request = HttpRequest()
        self.request.user = self.user
        self.form = PersonalInformationsForm(
            {"username": "Thomas", "biography": "Currently working on some projects."},
        )
        self.form.is_valid()
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.form.save(self.request)
        self.assertEqual(self.user.username, "Thomas")
