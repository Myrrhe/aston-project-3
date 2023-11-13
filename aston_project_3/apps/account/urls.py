"""The urls file"""
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from apps.account.forms import LoginForm
from apps.account.views import (
    AccountCreatedViewSet,
    AccountDeletedViewSet,
    AccountViewSet,
    AddSecurityKeyViewSet,
    CookiesPolicyViewSet,
    CookiesSettingsViewSet,
    DeleteAccountViewSet,
    HomeViewSet,
    SignupViewSet,
    StartViewSet,
)

app_name = "account"

urlpatterns = [
    path("", StartViewSet.as_view(), name="empty"),
    path("home/", HomeViewSet.as_view(), name="home"),
    re_path(
        r"^login/(?P<message>[a-z]*)$",
        auth_views.LoginView.as_view(
            template_name="registration/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path("signup/", SignupViewSet.as_view(), name="signup"),
    path("account_created/", AccountCreatedViewSet.as_view(), name="account-created"),
    path("account/", AccountViewSet.as_view(), name="account"),
    path("delete-account/", DeleteAccountViewSet.as_view(), name="delete-account"),
    path("account-deleted/", AccountDeletedViewSet.as_view(), name="account-deleted"),
    path("cookies-policy/", CookiesPolicyViewSet.as_view(), name="cookies-policy"),
    path(
        "cookies-settings/", CookiesSettingsViewSet.as_view(), name="cookies-settings"
    ),
    path("add-security-key/", AddSecurityKeyViewSet.as_view(), name="add-security-key"),
]
