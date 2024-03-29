"""The urls file."""
from django.urls import path
from apps.forum.views import (
    AnswerTopicViewSet,
    CreateTopicViewSet,
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
        "forum/main/<str:type_topic>/<str:category>/<int:page>",
        ForumViewSet.as_view(),
        name="forum-spec",
    ),
    path(
        "forum/topic/<uuid:topic_id>/<int:page>",
        TopicViewSet.as_view(),
        name="topic",
    ),
    path(
        "forum/topic/answer",
        AnswerTopicViewSet.as_view(),
        name="answer_topic",
    ),
    path(
        "forum/topic/create",
        CreateTopicViewSet.as_view(),
        name="create_topic",
    ),
]
