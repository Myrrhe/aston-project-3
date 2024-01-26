"""A timer to run a function periodically."""
from threading import Timer
from typing import Callable


class RepeatedTimer(object):
    """A timer to run a function periodically."""
    def __init__(self, interval: int, function: Callable, *args, **kwargs) -> None:
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self) -> None:
        """Run the function."""
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self) -> None:
        """Start the timer."""
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self) -> None:
        """Stop the timer."""
        self._timer.cancel()
        self.is_running = False
