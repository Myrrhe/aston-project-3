"""The command to regenerate the secret key."""
from django.core.management.base import BaseCommand, CommandParser
from django.core.management.utils import get_random_secret_key

from apps.core.utils.create_secret_key_util import create_django_key


class Command(BaseCommand):
    """The command toregenerate the secret key."""

    help = "Regenerate a secret key"

    def add_arguments(self, parser: CommandParser) -> None:
        """Add arguments to the command."""
        parser.add_argument(
            "--auto",
            action="store_true",
            help="Automatically change the secret key of the .env file",
        )

    def handle(self, *args, **options) -> None:
        """Execute the code when the command is called."""
        if options["auto"]:
            django_key = create_django_key()
            new_env = []
            with open("aston_project_3/.env", "r", encoding="utf-8") as file:
                for line in file:
                    if line.startswith("SECRET_KEY="):
                        line = f"SECRET_KEY={django_key}"
                    new_env.append(line)
            with open("aston_project_3/.env", "w", encoding="utf-8") as file:
                for line in new_env:
                    file.write(line)
                file.write("\n")
            print("The secret key has been regenerated")
            if options["verbosity"] > 1:
                print(django_key)
        else:
            print(get_random_secret_key())
