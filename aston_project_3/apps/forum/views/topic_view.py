"""The topic view."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from math import ceil

from apps.forum.forms import AnswerTopicForm
from apps.forum.models import Topic


class TopicViewSet(View):
    """The topic view."""

    def get(
        self,
        request: HttpRequest,
        topic_id: str,
        page: int = 1,
        *args,
        **kwargs,
    ) -> HttpResponse:
        """GET method."""
        topic = Topic.objects.get(pk=topic_id)
        nb_pages = ceil(topic.get_replies / 10)
        if nb_pages < 1:
            nb_pages = 1
        if page < 0:
            page = 1
        elif page == 0 or page > nb_pages:
            page = nb_pages
        posts = topic.posts.order_by("created_at")[(page - 1) * 10 : page * 10]
        topic.increment_view()
        return render(
            request,
            "forum/topic.html",
            context={
                "topic": topic,
                "posts": posts,
                "page": page,
                "nb_pages": nb_pages,
                "page_first": page == 1,
                "page_greater_than_two": page > 2,
                "page_lesser_than_penultimate": page < nb_pages - 1,
                "page_last": page == nb_pages,
                "next_page": page + 1,
                "prev_page": page - 1,
                "answer_form": AnswerTopicForm(initial={"topic_id": topic_id}),
            },
        )
