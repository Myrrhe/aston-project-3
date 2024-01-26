"""The command to launch the tests."""
import subprocess
import webbrowser
from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    """The command to launch the tests."""

    help = "Regenerate a secret key"

    def add_arguments(self, parser: CommandParser) -> None:
        """Add arguments to the command."""
        parser.add_argument(
            "--open",
            action="store_true",
            help="Open the coverage file",
        )
        parser.add_argument(
            "--notests",
            action="store_true",
            help="Make that tests aren't executed",
        )
        parser.add_argument(
            "--module",
            type=str,
            help="Specify a module to test alone",
        )

    def handle(self, *args, **options) -> None:
        """Execute the code when the command is called."""
        if not options["notests"]:
            if options["module"] is None:
                subprocess.run("coverage run manage.py test", shell=False, check=False)
            else:
                subprocess.run(
                    f"coverage run manage.py test {options["module"]}",
                    shell=False,
                    check=False
                )
            subprocess.run("coverage html", shell=False, check=True)
            subprocess.run("coverage xml", shell=False, check=True)
        if options["open"]:
            webbrowser.register(
                "firefox",
                None,
                webbrowser.BackgroundBrowser("C:/Program Files/Mozilla Firefox/firefox.exe")
            )
            webbrowser.get("firefox").open_new_tab(f"file://{settings.BASE_DIR}/htmlcov/index.html")
