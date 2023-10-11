from django.urls import path, include
from apps.account.views import HomeViewSet

# from rest_framework.routers import DefaultRouter

from apps.account.views import HomeViewSet

# router = DefaultRouter()

# router.register(r"home", HomeViewSet, basename="home")

urlpatterns = [
    path("", HomeViewSet.as_view(), name="home"),
]
