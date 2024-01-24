"""The command to delete all matches from the database."""
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    """The command to delete all matches from the database."""

    help = "Delete all matches from the database"

    def add_arguments(self, parser: CommandParser) -> None:
        """Add arguments to the command."""
        parser.add_argument(
            "--leaveone",
            action="store_true",
            help="Leave one match",
        )

    def handle(self, *args, **options) -> None:
        """Execute the code when the command is called."""
