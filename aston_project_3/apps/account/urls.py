"""The urls file"""
from django.urls import path, include

from apps.account.views import AccountCreatedViewSet
from apps.account.views import HomeViewSet
from apps.account.views import SignupViewSet
from apps.account.views import StartViewSet

urlpatterns = [
    path("", StartViewSet.as_view(), name="empty"),
    path("home/", HomeViewSet.as_view(), name="home"),
    path("signup/", SignupViewSet.as_view(), name="signup"),
    path("account_created/", AccountCreatedViewSet.as_view(), name="account-created"),
]
