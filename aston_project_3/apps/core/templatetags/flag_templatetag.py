"""Get a flag emoji from a country code."""
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name="flag")
@stringfilter
def flag(value: str) -> str:
    """Get a flag emoji from a country code."""
    if value:
        if value == "en":
            value = "gb"
        code_points = [127397 + ord(char) for char in value.upper()]
        return "".join([chr(c) for c in code_points])
    return ""
