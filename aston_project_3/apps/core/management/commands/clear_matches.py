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
        if not options["notests"]:
            subprocess.run("coverage run manage.py test", shell=False)
            subprocess.run("coverage html", shell=False)
            subprocess.run("coverage xml", shell=False)
        if options["open"]:
            webbrowser.register(
                "firefox",
                None,
                webbrowser.BackgroundBrowser("C:/Program Files/Mozilla Firefox/firefox.exe")
            )
            webbrowser.get("firefox").open_new_tab(f"file://{settings.BASE_DIR}/htmlcov/index.html")
