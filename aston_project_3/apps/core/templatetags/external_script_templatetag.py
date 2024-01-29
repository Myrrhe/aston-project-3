"""Get a prefixed SHA code for an external script."""
from django import template

register = template.Library()


@register.filter(name="external_script")
def external_script(value: dict[str]) -> str:
    """Get a prefixed SHA code for an external script."""
    return "-".join([value["algorithm"], value["sha"]])
