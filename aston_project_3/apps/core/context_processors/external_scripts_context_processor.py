"""The context processor for external scripts."""
from django.conf import settings
from django.http import HttpRequest


def external_scripts(_: HttpRequest) -> dict[dict[str]]:
    """The context processor for external scripts."""
    return {"EXTERNAL_SCRIPTS": settings.EXTERNAL_SCRIPTS}
