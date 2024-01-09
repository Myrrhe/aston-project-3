"""The answer topic form."""
from django.forms import ValidationError
from django.http import HttpRequest
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _

from django import forms

from apps.forum.models import Post, Topic


class AnswerTopicForm(forms.Form):
    """The answer topic form."""

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control p-3 textarea-answer",
                "placeholder": _("your_answer"),
                "id": "content",
            },
        ),
        label=_("answer"),
    )
    topic_id = forms.UUIDField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control d-none",
                "id": "topic",
            },
        ),
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str]:
        """Clean the form."""
        if "content" not in self.data:
            raise ValidationError(
                _("missing_field"),
                code="missing_field",
            )
        self.cleaned_data["content"] = escape(self.cleaned_data["content"])
        return self.cleaned_data

    def save(self, request: HttpRequest) -> None:
        """Save the data of the form."""
        Post.objects.create(
            user=request.user,
            topic=Topic.objects.get(pk=self.cleaned_data["topic_id"]),
            content=self.cleaned_data["content"],
        )

    class Meta(object):
        """The meta class."""

        model = Post
        fields = (
            "content",
            "topic_id",
        )
