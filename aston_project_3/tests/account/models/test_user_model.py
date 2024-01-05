"""The tests for the user model"""

from django.test import TransactionTestCase

from apps.account.models import User


class TestUserModel(TransactionTestCase):
    """The tests for the user model"""

    def test_standard(self) -> None:
        """Run the tests"""
        with self.assertRaises(TypeError, msg="Users must have an email address."):
            User.objects.create_user(None)
        user = User.objects.create_user("test@user_model.com", password="123456")
        with self.assertRaises(TypeError, msg="Superusers must have a password."):
            User.objects.create_superuser("test_super_nopassword@user_model.com", None)
        User.objects.create_superuser("test_super@user_model.com", "123456")
        self.assertEqual(
            user.id, User.objects.get_by_natural_key("test@user_model.com").id
        )
        self.assertFalse(user.is_staff)
        self.assertEqual(user.get_name, user.email)
        user.username = "Thomas"
        user.save()
        self.assertEqual(user.get_name, user.username)
        self.assertFalse(user.has_module_perms("account"))
        self.assertFalse(user.has_perm("admin"))
        self.assertFalse(user.has_security_key())
        self.assertTrue(user.check_security_key("123456"))
        self.assertTrue(user.check_credentials("123456", "123456"))
        self.assertTrue(user.is_bot_name_available("Bot 1"))
        self.assertEqual(user.natural_key(), (user.email,))
        self.assertEqual(str(user), user.email)
