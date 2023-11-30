"""A string concatenator."""
from django import template

register = template.Library()


@register.filter
def addstr(arg1: str, arg2: str) -> str:
    """Concatenate arg1 & arg2."""
    return str(arg1) + str(arg2)
