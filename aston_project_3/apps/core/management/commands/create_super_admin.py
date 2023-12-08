"""The command to create a superuser."""
from django.core.management.base import BaseCommand

from apps.account.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice

from base64 import b32encode


class Command(BaseCommand):
    """The command to create a superuser."""

    help = "Create super user if one doesn't exists"

    def handle(self, *args, **options) -> None:
        """Execute the code when the command is called."""
        if not User.objects.filter(is_superuser=True).first():
            user = User.objects.create(
                email="admin@aston.com", is_superuser=True, is_admin=True
            )
            user.set_password("admin")
            user.save()

            totp = TOTPDevice.objects.create(
                name="admin_key",
                user_id=user.id,
            )
            print(
                f"The key of the admin is\n{b32encode(totp.bin_key).decode('utf-8')}"
            )

            code = input("Enter a 6 digits code to test the security key :")

            if totp.verify_token(code):
                print("The security key work properly")
            else:
                print("Error: code not working")
        else:
            print("Super admin already created")
