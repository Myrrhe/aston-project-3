"""Get a form with a prefix."""
from django.forms import Form
from django.http import HttpRequest


def get_form(
        request: HttpRequest,
        formcls: Form,
        prefix: str,
        *args,
        **kwargs
    ) -> Form:
    """Get a form with a prefix."""
    data = request.POST if prefix in request.POST else None
    return formcls(data, *args, prefix=prefix, **kwargs)
