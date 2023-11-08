"""A function to get a form with a prefix"""


def get_form(request: any, formcls: any, prefix: str) -> any:
    """A function to get a form with a prefix"""
    data = request.POST if prefix in request.POST else None
    return formcls(data, prefix=prefix)
