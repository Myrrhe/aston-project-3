"""Non-sticky input."""
from django.forms import TextInput


class NonStickyTextInput(TextInput):
    """
    Custom text input widget that's "non-sticky".

    (i.e. does not remember submitted values).
    """

    def get_context(
        self,
        name: str,
        _: str,
        attrs: any,
    ) -> dict[str, dict[str, any]]:
        """Clear the submitted value."""
        return super().get_context(name, None, attrs)
