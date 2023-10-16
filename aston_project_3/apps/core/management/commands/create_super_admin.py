"""The command to create a superuser"""
from django.core.management.base import BaseCommand

from apps.account.models import User


class Command(BaseCommand):
    """The command to create a superuser"""

    help = "Create super user if not exist "

    def handle(self, *args, **options) -> None:
        if not User.objects.filter(is_superuser=True).first():
            user = User.objects.create(
                email="admin@aston.com", is_superuser=True, is_admin=True
            )
            user.set_password("admin")
            user.save()
        else:
            print("Super admin already created")
