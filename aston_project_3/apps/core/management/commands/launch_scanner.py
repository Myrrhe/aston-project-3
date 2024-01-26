"""The command to launch the SonarCloud scanner."""
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """The command to launch the SonarCloud scanner."""

    help = "Launch the SonarCloud scanner"

    def handle(self, *args, **options) -> None:
        """Execute the code when the command is called."""
        subprocess.run(
            ["sonar-scanner", f"-Dtoken={settings.SONAR_TOKEN}"],
            shell=True,
            cwd="..",
            check=True
        )
