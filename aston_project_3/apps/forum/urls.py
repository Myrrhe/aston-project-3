"""The urls file."""
from django.urls import path
from apps.forum.views import (
    ForumViewSet,
    TopicViewSet,
)

app_name = "forum"

urlpatterns = [
    path(
        "forum/main",
        ForumViewSet.as_view(),
        name="forum-start",
    ),
    path(
        "forum/main/<str:type>/<str:category>/<int:page>",
        ForumViewSet.as_view(),
        name="forum-spec",
    ),
    path(
        "forum/topic/<uuid:topic_id>/<int:page>",
        TopicViewSet.as_view(),
        name="topic",
    ),
]
