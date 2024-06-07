"""The urls file."""
from django.urls import path

from apps.core.views import GetCSRFViewSet
from apps.core.views import SetLanguageViewSet

urlpatterns = [
    path("set-language", SetLanguageViewSet.as_view(), name="set-language"),
    path("get-csrf", GetCSRFViewSet.as_view(), name="get-csrf"),
]
