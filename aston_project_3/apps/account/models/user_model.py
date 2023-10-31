"""The user's model"""
from __future__ import annotations

import urllib
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from django.utils.translation import gettext as _

from django_otp.plugins.otp_totp.models import TOTPDevice

from apps.core.models.timestamped_model import TimestampedModel

# from apps.core.tokens import encode_token


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, email: str, password: str = None) -> User:
        """Create and return a `User` with an email, username and password."""
        if email is None:
            raise TypeError("Users must have an email address.")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str) -> User:
        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_admin = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    """The user's model"""

    LANGUAGES_CHOICES = [
        ("EN", "English"),
        ("FR", "Français"),
        ("ES", "Español"),
    ]

    DARK_CHOICES = [
        ("DARK", 0),
        ("LIGHT", 1),
        ("AUTO", 2),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("email"),
        help_text=_("email_help_text"),
    )
    username = models.CharField(
        max_length=50,
        null=True,
        blank=False,
        verbose_name=_("username"),
        help_text=_("username_help_text"),
    )
    language = models.CharField(
        max_length=2,
        choices=LANGUAGES_CHOICES,
        default="FR",
    )
    theme = models.IntegerField(
        choices=DARK_CHOICES,
        default="AUTO",
    )
    is_email_confirmed = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        verbose_name=_("is_email_confirmed"),
        help_text=_("is_email_confirmed_help_text"),
    )
    is_tou_accepted = models.BooleanField(
        default=False,
        verbose_name=_("is_tou_accepted"),
        help_text=_("is_tou_accepted_help_text"),
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name=_("is_admin"),
        help_text=_("is_admin_help_text"),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta(TimestampedModel.Meta):
        """The meta class"""

        db_table = "user"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def is_staff(self) -> bool:
        return self.is_admin

    def has_module_perms(self, app_label: str) -> bool:
        return self.is_staff

    def has_perm(self, perm: str, obj: object = None) -> bool:
        return self.is_staff

    # def send_email_confirmation(self, template, path, email):
    #     email_key = "newEmail" if email is not None else "email"
    #     email = email if email is not None else self.email
    #     token = encode_token(
    #         {"email": email, "current_email": self.email}
    #     )
    #     print(token)

    #     params = {"token": token, f"{email_key}": email}

    #     referer = current_request().META.get("HTTP_REFERER")
    #     language = (
    #         current_request()
    #         .headers.get("Accept-Language")
    #         .split(", ")[0]
    #     )

    #     SendgridMailer.send_mail(
    #         email,
    #         template,
    #         {
    #             "firstname": self.firstname,
    #             "url": f"{referer}{language}/{path}?{urllib.parse.urlencode(params)}",  # noqa
    #             "email": email,
    #         },
    #     )

    def __str__(self) -> str:
        return f"{self.email}"
