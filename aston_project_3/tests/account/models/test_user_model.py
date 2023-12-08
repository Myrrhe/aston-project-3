"""The tests for the user model"""

from django.test import TransactionTestCase

from apps.account.models import User
from apps.account.models.user_model import UserManager


class TestUserModel(TransactionTestCase):
    """The tests for the user model"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.user_manager = UserManager()
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        with self.assertRaises(TypeError, msg="Users must have an email address."):
            self.user_manager.create_user(None)
        user = self.user_manager.create_user("test@user_model.com", password="123456")
        with self.assertRaises(TypeError, msg="Superusers must have a password."):
            self.user_manager.create_user(None, 123456)
        superuser = self.user_manager.create_superuser("test@user_model.com", "123456")
        # self.assertEqual(self.answer.__str__(), "I am : 18-28 years old")
