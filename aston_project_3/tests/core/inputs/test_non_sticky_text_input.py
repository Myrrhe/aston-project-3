"""The tests for the non sticky text input"""
from django.test import TransactionTestCase

from apps.core.inputs import NonStickyTextInput


class TestNonStickyTextInput(TransactionTestCase):
    """The tests for the non sticky text input"""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.non_sticky_text_input = NonStickyTextInput()
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        self.assertEqual(
            self.non_sticky_text_input.get_context("machin", "truc", None),
            {
                "widget": {
                    "name": "machin",
                    "is_hidden": False,
                    "required": False,
                    "value": None,
                    "attrs": {},
                    "template_name": "django/forms/widgets/text.html",
                    "type": "text",
                }
            },
        )
