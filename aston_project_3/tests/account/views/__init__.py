"""The module file."""
from .test_account_created_view import TestAccountCreatedView
from .test_account_deleted_view import TestAccountDeletedView
from .test_cookies_policy_view import TestCookiesPolicyView
from .test_cookies_settings_view import TestCookiesSettingsView
from .test_delete_account_view import TestDeleteAccountView
from .test_home_view import TestHomeView
from .test_signup_view import TestSignupView
from .test_start_view import TestStartView

__all__ = [
    "TestAccountCreatedView",
    "TestAccountDeletedView",
    "TestCookiesPolicyView",
    "TestCookiesSettingsView",
    "TestDeleteAccountView",
    "TestHomeView",
    "TestSignupView",
    "TestStartView",
]
