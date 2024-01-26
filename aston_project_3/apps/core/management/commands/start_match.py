"""The command to start a match between two bots."""
from django.core.management.base import BaseCommand

from apps.game.models import Match


class Command(BaseCommand):
    """The command to start a match between two bots."""

    help = "Start a match between two bots"

    def handle(self, *args, **options) -> None:
        """Execute the code when the command is called."""
        Match.objects.start_match()
