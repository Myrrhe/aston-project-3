"""The forum view."""
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from apps.forum.models import Topic, TopicSection


class ForumViewSet(View):
    """The forum view."""

    def get(
        self,
        request: HttpRequest,
        type: str = "all",
        category: str = "new",
        page: int = 1,
        *args,
        **kwargs,
    ) -> HttpResponse:
        """GET method."""
        topics = None
        match type:
            case "all":
                topics = Topic.objects.order_by("-created_at")[
                    (page - 1) * 10 : page * 10
                ]
            case _:
                print("error")
        sections = TopicSection.objects.all()
        return render(
            request,
            "forum/forum.html",
            context={
                "topics": topics,
                "sections": sections,
            },
        )
