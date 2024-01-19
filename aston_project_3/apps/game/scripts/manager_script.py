"""Signals for the automated matchs."""
from datetime import datetime

from django.utils.translation import gettext_lazy as _


from apps.core.utils import RepeatedTimer
from django.core.management import call_command


class ScriptManager(object):
    """The config class."""

    auto_match_started = False
    auto_match_ended = False
    script = None
    timer = None

    @staticmethod
    def start_external_script():
        if not ScriptManager.auto_match_started:
            ScriptManager.auto_match_started = True
            ScriptManager.timer = RepeatedTimer(5, lambda : call_command("start_match"))

    @staticmethod
    def stop_external_script():
        if not ScriptManager.auto_match_ended:
            ScriptManager.auto_match_ended = True
            ScriptManager.timer.stop()
    
    @staticmethod
    def test():
        with open("AlphaGamma.py", "w", encoding="utf-8") as file:
            file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
