"""The module file"""
from .account_created_view import AccountCreatedViewSet
from .account_view import AccountViewSet
from .cookies_policy_view import CookiesPolicyViewSet
from .cookies_settings_view import CookiesSettingsViewSet
from .home_view import HomeViewSet
from .signup_view import SignupViewSet
from .start_view import StartViewSet

__all__ = [
    "AccountCreatedViewSet",
    "AccountViewSet",
    "CookiesPolicyViewSet",
    "CookiesSettingsViewSet",
    "HomeViewSet",
    "SignupViewSet",
    "StartViewSet",
]
