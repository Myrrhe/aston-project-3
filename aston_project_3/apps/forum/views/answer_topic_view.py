"""The answer topic view."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views import View

from apps.forum.forms import AnswerTopicForm


class AnswerTopicViewSet(View):
    """The answer topic view."""

    def post(
        self,
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> HttpResponse:
        """POST method."""
        answer_form = AnswerTopicForm(request.POST)
        if answer_form.is_valid():
            answer_form.save(request)
        return redirect("forum:topic", topic_id=request.POST["topic_id"], page="0")
