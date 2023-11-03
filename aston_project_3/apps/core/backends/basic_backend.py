"""The backend authentication"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp import verify_token

from apps.account.models import User

UserModel = get_user_model()


class BasicBackend(BaseBackend):
    """The backend authentication class"""

    def authenticate(
        self, request: HttpRequest, username: str = None, password: str = None, **kwargs
    ) -> any:
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
                if request.path == "/login/":
                    print("Logging via non-admin")
                    if TOTPDevice.objects.filter(user_id=user.id).exists():
                        # The user have a security key
                        if verify_token(
                            user,
                            TOTPDevice.objects.get(user_id=user.id).persistent_id,
                            request.POST["security_key"],
                        ):
                            return user
                        else:
                            print("Wrong code")
                            return
                    else:
                        # The user don't have a security key
                        return user
                elif request.path == "/admin/login/":
                    print("Logging via admin")
                    if TOTPDevice.objects.filter(user_id=user.id).exists():
                        # The user have a security key
                        if verify_token(
                            user,
                            TOTPDevice.objects.get(user_id=user.id).persistent_id,
                            request.POST["security_key"],
                        ):
                            return user
                        else:
                            print("Wrong code")
                            return
                    else:
                        # The user don't have a security key
                        print("No security key")
                        return
                else:
                    print("Logging via unknown")
                    return

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
