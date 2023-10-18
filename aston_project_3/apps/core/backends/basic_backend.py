"""The backend authentication"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest

from apps.account.models import User

UserModel = get_user_model()


class BasicBackend(BaseBackend):
    """The backend authentication class"""

    def authenticate(
        self, request: HttpRequest, username: str = None, password: str = None, **kwargs
    ) -> any:
        if request.path == "/login/":
            print("Logging via non-admin")
        elif request.path == "/admin/login/":
            print("Logging via admin")
        else:
            print("Logging via unknown")
        if "security_key" in request.POST:
            print(request.POST["security_key"])
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user.
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id: str) -> any:
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

    def user_can_authenticate(self, user: User) -> any:
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        return getattr(user, "is_active", True)
