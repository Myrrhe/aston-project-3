"""The command to load the production fixtures."""
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandParser
from django.db.models import Model
from django.db.utils import IntegrityError

from apps.core.utils.json_processing_util import count_instance
from apps.forum.models import (
    Post,
    Topic,
    TopicSection,
)


class Command(BaseCommand):
    """
    The command to load the production fixtures.

    Exemple :
    python manage.py create_production_fixtures --add
    """

    help = "Create fixtures on first deploy"
    requires_migrations_checks = True
    verbosity = 0
    add = False
    test = False
    is_working = True

    def add_arguments(self, parser: CommandParser) -> None:
        """Add arguments to the command."""
        parser.add_argument(
            "--add",
            action="store_true",
            help="Add objects even if some of the same type already exist",
        )
        parser.add_argument(
            "--test",
            action="store_true",
            help="Run the command without loading the fixtures",
        )

    def handle(self, *args, **options) -> None:
        """Execute the code when the command is called."""
        self.log("Loading fixtures")
        Command.verbosity = options["verbosity"]
        Command.add = options["add"]
        Command.test = options["test"]

        self.loading_model(TopicSection, True)
        self.loading_model(Topic, True)
        self.loading_model(Post, True)
        if Command.is_working:
            self.log(self.style.SUCCESS("Fixtures loading terminated without errors"))
        else:
            self.log(self.style.ERROR_OUTPUT("Fixtures loading failed"))

    def loading_model(self, model: Model, strict: bool) -> None:
        """Load one model's fixture file."""
        if Command.is_working:
            path = (
                model.__module__.replace(".", "/").replace("model", "fixture")
                + "s.json"
            )
            if model.objects.all().count() <= 0:
                # The table for this model is empty
                self.log("Creating", self.style.SQL_TABLE(model.__name__), "...")
                self.load_fixture_file(path)
            elif Command.add or not strict:
                # The table is not empty, but we added "--add" to bypass it
                self.log("Updating", self.style.SQL_TABLE(model.__name__), "...")
                self.load_fixture_file(path)
            elif count_instance(path) > model.objects.all().count():
                # The table is half-created
                self.log_err(
                    self.style.ERROR_OUTPUT("Error:"),
                    self.style.SQL_TABLE(model.__name__),
                    "are already half created",
                )
                Command.is_working = False
            elif count_instance(path) == model.objects.all().count():
                # The table is already created
                self.log(self.style.SQL_TABLE(model.__name__), "already created")
            else:
                # The table somehow contain too many elements
                self.log(
                    self.style.WARNING("Warning:"),
                    self.style.SQL_TABLE(model.__name__),
                    "contains more elements than its corresponding fixture",
                )
            if not Command.is_working:
                self.log(
                    self.style.NOTICE(
                        "Aborting the rest of the fixtures loading because of error"
                    )
                )
        else:
            self.log("Skipping", self.style.SQL_TABLE(model.__name__))

    def load_fixture_file(self, path: str) -> str:
        """Load one fixture file."""
        if not Command.test:
            try:
                call_command("loaddata", path, f"--verbosity={Command.verbosity}")
            except IntegrityError as e:
                Command.is_working = False
                self.log_err(self.style.ERROR_OUTPUT("IntegrityError:"), e)

    def log(self, *string, importance: int = 1, **kwargs) -> None:
        """Log a message."""
        if Command.verbosity >= importance:
            self.stdout.write(" ".join(string))

    def log_err(self, *string, importance: int = 1, **kwargs) -> None:
        """Log an error message."""
        if Command.verbosity >= importance:
            self.stderr.write(" ".join(string))
