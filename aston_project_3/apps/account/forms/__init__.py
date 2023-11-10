"""The module file"""
from .change_email_form import ChangeEmailForm
from .change_password_form import ChangePasswordForm
from .create_security_key_form import CreateSecurityKeyForm
from .login_form import LoginForm
from .personal_informations_form import PersonalInformationsForm
from .signup_form import SignupForm

__all__ = [
    "ChangeEmailForm",
    "ChangePasswordForm",
    "CreateSecurityKeyForm",
    "LoginForm",
    "PersonalInformationsForm",
    "SignupForm",
]
