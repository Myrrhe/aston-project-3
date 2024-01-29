"""The command to check the sri hash of the imported scripts."""
import hashlib
import requests

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    """The command to check the sri hash of the imported scripts."""

    help = "Check the sri hash of the imported scripts"

    def add_arguments(self, parser: CommandParser) -> None:
        """Add arguments to the command."""

    def handle(self, *args, **options) -> None:
        """Execute the code when the command is called."""
        expired_sha = False
        for key, value in settings.EXTERNAL_SCRIPTS_URL.items():
            try:
                response = requests.get(value["url"], timeout=10)
                response.raise_for_status()

                content = response.text
                status = response.status_code
            except requests.exceptions.RequestException as e:
                print(f"Erreur lors de la récupération du script : {e}")
            if status == 200:
                actual_hash = hashlib.sha256(content.encode()).hexdigest()
                if actual_hash != value["sha"]:
                    expired_sha = True
                    print(f"Le script {key} a une clef SHA périmée. Clef SHA correct :\n{actual_hash}")
        if not expired_sha:
            print("Toutes les clef SHA des scripts externes sont correctes.")
