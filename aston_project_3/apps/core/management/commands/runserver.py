"""The customized start/end command."""
import atexit
import os
import signal
import sys

from django.core.management.commands.runserver import Command as BaseRunServerCommand
from django.conf import settings

from apps.game.scripts import ScriptManager


class Command(BaseRunServerCommand):
    """The customized start/end command."""
    def __init__(self, *args, **kwargs) -> None:
        atexit.register(self._exit)
        signal.signal(signal.SIGINT, self._handle_SIGINT)
        super().__init__(*args, **kwargs)

    def _exit(self) -> None:
        """Called at the end of the server."""
        if settings.MATCH_AUTO == "1" and os.environ.get("RUN_MAIN") is None and "runserver" in sys.argv:
            ScriptManager.stop_external_script()

    def _handle_SIGINT(self, signal, frame) -> None:
        """Needed to handle the end."""
        self._exit()
        sys.exit(0)
