"""The command to check the sri hash of the imported scripts."""
import base64
import hashlib
import requests

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser

from apps.core.templatetags.external_script_templatetag import external_script


class Command(BaseCommand):
    """The command to check the sri hash of the imported scripts."""

    help = "Check the sri hash of the imported scripts"

    def add_arguments(self, parser: CommandParser) -> None:
        """Add arguments to the command."""

    def handle(self, *args, **options) -> None:
        """Execute the code when the command is called."""
        expired_sha = False
        for key, value in settings.EXTERNAL_SCRIPTS.items():
            try:
                response = requests.get(value["url"], timeout=10)
                response.raise_for_status()

                content = response.text
                status = response.status_code
            except requests.exceptions.RequestException as e:
                print(f"Erreur lors de la récupération du script : {e}")
            if status == 200:
                new_key_required = False
                string_key_message = "Le script {name} a une clef SHA périmée. Clef SHA correct :\n{new_hash}\n"
                if value["algorithm"] not in ["sha256", "sha384", "sha512"]:
                    new_key_required = True
                    expired_sha = True
                    print(f"Le script {key} n'a pas d'algorithme autorisé. "
                          "Algorithmes autorisés : sha256, sha384, sha512")
                    value["algorithm"] = "sha512"
                    string_key_message = "Nouvelle clef SHA pour {name} :\n{new_hash}\n"
                hash_method = None
                match value["algorithm"]:
                    case "sha256":
                        hash_method = hashlib.sha256
                    case "sha384":
                        hash_method = hashlib.sha384
                    case "sha512":
                        hash_method = hashlib.sha512
                    case _:
                        hash_method = hashlib.sha256
                actual_hash = {
                    "sha": base64.b64encode(
                        hash_method(content.encode("utf-8")).digest()
                    ).decode("utf-8"),
                    "algorithm": value["algorithm"],
                }
                if external_script(actual_hash) != external_script(value):
                    new_key_required = True
                    expired_sha = True
                if new_key_required:
                    print(string_key_message.format(**{"name": key, "new_hash": external_script(actual_hash)}))
        if not expired_sha:
            print("Toutes les clef SHA des scripts externes sont correctes.")
