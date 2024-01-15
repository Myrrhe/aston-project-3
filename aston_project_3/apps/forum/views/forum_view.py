"""The forum view."""
from math import ceil

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from apps.forum.models import Topic, TopicSection


class ForumViewSet(View):
    """The forum view."""

    def get(
        self,
        request: HttpRequest,
        type_topic: str = "all",
        category: str = "new",
        page: int = 1,
    ) -> HttpResponse:
        """GET method."""
        topics = Topic.objects.filter(deleted=False)
        if type_topic != "all":
            topics = topics.filter(section__code=type_topic)
        match category:
            case "new":
                topics = topics.order_by("-created_at")
            case "old":
                topics = topics.order_by("created_at")
            case _:
                return redirect("forum:forum-start")
        sections = TopicSection.objects.all()
        nb_topics = topics.count()
        nb_pages = max(ceil(nb_topics / 10), 1)
        if page < 1:
            page = 1
        elif page > nb_pages:
            page = nb_pages
        topics = topics[(page - 1) * 10:page * 10]
        return render(
            request,
            "forum/forum.html",
            context={
                "topics": topics,
                "type_topic": type_topic,
                "sections": sections,
                "category": category,
                "page": page,
                "nb_pages": nb_pages,
                "nb_topics": nb_topics,
                "page_first": page == 1,
                "page_greater_than_two": page > 2,
                "page_lesser_than_penultimate": page < nb_pages - 1,
                "page_last": page == nb_pages,
                "next_page": page + 1,
                "prev_page": page - 1,
            },
        )
