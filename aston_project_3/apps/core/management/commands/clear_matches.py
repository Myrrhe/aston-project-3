"""The command to delete all matches from the database."""
from django.core.management.base import BaseCommand, CommandParser

from apps.game.models import Match


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
        matches = Match.objects.all()
        if not matches.exists():
            print("No match in the database.")
            return
        if options["leaveone"]:
            print(matches.count())
            one_match = matches.order_by("?").first()
            matches = matches.exclude(id=one_match.id)
            print(matches.count())
        count = matches.count()
        matches.delete()
        print(f"{count} matches have been deleted from the database.")
