"""The urls file"""
from django.urls import path

from apps.core.views import SetLanguageViewSet

urlpatterns = [
    path("set-language", SetLanguageViewSet.as_view(), name="set-language"),
]
