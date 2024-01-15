"""A method to mute stdout. For exemple when calling command via call_command."""
import sys
from contextlib import contextmanager
from typing import Generator

from apps.core.utils.none_return_util import return_none

@contextmanager
def silence_stdout(
    stdout: bool = False,
    stderr: bool = False,
    django_stdout: bool = False,
    django_stderr: bool = False,
) -> Generator[None, None, None]:
    """
    Mute the standard output. Is used as follows :

    with silence_stdout():
        ... # Do stuff
    """
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    original_django_stdout_write = sys.stdout.write
    original_django_stderr_write = sys.stderr.write
    try:
        if stdout:
            sys.stdout = open("nul" if sys.platform.startswith("win") else "/dev/null", "w")
        if stderr:
            sys.stderr = open("nul" if sys.platform.startswith("win") else "/dev/null", "w")
        if django_stdout:
            sys.stdout.write = return_none
        if django_stderr:
            sys.stderr.write = return_none
        yield
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        sys.stdout.write = original_django_stdout_write
        sys.stderr.write = original_django_stderr_write
