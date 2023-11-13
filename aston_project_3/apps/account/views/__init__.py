"""The module file"""
from .account_created_view import AccountCreatedViewSet
from .account_deleted_view import AccountDeletedViewSet
from .account_view import AccountViewSet
from .add_security_key_view import AddSecurityKeyViewSet
from .cookies_policy_view import CookiesPolicyViewSet
from .cookies_settings_view import CookiesSettingsViewSet
from .delete_account_view import DeleteAccountViewSet
from .home_view import HomeViewSet
from .signup_view import SignupViewSet
from .start_view import StartViewSet

__all__ = [
    "AccountCreatedViewSet",
    "AccountDeletedViewSet",
    "AccountViewSet",
    "AddSecurityKeyViewSet",
    "CookiesPolicyViewSet",
    "CookiesSettingsViewSet",
    "DeleteAccountViewSet",
    "HomeViewSet",
    "SignupViewSet",
    "StartViewSet",
]
