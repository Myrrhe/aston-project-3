"""The topic creation view."""
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from apps.forum.forms import CreateTopicForm
from apps.forum.models import Topic


class CreateTopicViewSet(CreateView):
    """The topic creation view."""

    model = Topic
    form_class = CreateTopicForm
    template_name = "forum/create_topic.html"

    def get_success_url(self, **kwargs) -> any:
        """Determine where the user is redirected on success."""
        print(kwargs)
        return reverse_lazy(
            "forum:forum-start",
        )

    def get_context_data(self, **kwargs) -> any:
        """Send additionnal data to the template."""
        context = super().get_context_data(**kwargs)
        return context

    def get_form_kwargs(self) -> any:
        """Add additionnal kwargs to the form."""
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs
