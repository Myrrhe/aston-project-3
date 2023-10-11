"""The urls file"""
from django.urls import path, include
from apps.account.views import HomeViewSet

from apps.account.views import HomeViewSet

urlpatterns = [
    path("", HomeViewSet.as_view(), name="home"),
]
