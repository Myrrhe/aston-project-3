"""The topic creation form."""
from django.forms import ModelForm, ValidationError
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from django import forms

from apps.forum.models import Post, Topic, TopicSection


class CreateTopicForm(ModelForm):
    """The topic creation form."""

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("topic_title"),
                "id": "title",
            },
        ),
        label=_("title"),
    )

    section = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "section",
            },
        ),
        label=_("section"),
        choices=TopicSection.get_all(),
    )

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": _("topic_post"),
                "id": "content",
            },
        ),
        label=_("content"),
    )

    def __init__(self, *args, **kwargs) -> None:
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str]:
        """Clean the form."""
        return self.cleaned_data

    def save(self) -> None:
        """Save the data of the form."""
        sections = TopicSection.objects.filter(code=self.cleaned_data["section"])
        topic = Topic.objects.create(
            user=self.request.user,
            title=self.cleaned_data["title"],
            section=sections[0],
        )
        Post.objects.create(
            user=self.request.user,
            topic=topic,
            content=self.cleaned_data["content"],
        )

    class Meta(object):
        """The meta class."""

        model = Topic
        fields = (
            "title",
            "title",
            "content",
        )
