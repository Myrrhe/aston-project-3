"""The user's model."""
from __future__ import annotations

import urllib
import uuid

from django.conf import settings

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from django.utils.translation import gettext as _

from django_otp import verify_token
from django_otp.plugins.otp_totp.models import TOTPDevice

from apps.core.models import TimestampedModel

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

    def get_by_natural_key(self, email: str = "admin@aston.com") -> User:
        """Get a user by their email."""
        return self.get(email=email)


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    """The user's model."""

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
        blank=True,
        verbose_name=_("username"),
        help_text=_("username_help_text"),
    )
    biography = models.CharField(
        max_length=60,
        null=True,
        blank=False,
        verbose_name=_("biography"),
        help_text=_("biography_help_text"),
    )
    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES,
        default="fr",
    )
    theme = models.CharField(
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
        """The meta class."""

        db_table = "user"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def is_staff(self) -> bool:
        """Check if the user is a staff member."""
        return self.is_admin

    @property
    def get_name(self) -> str:
        """Get the username ot the email."""
        return self.username if self.username else self.email

    def has_module_perms(self, app_label: str) -> bool:
        """Needed for the admin part."""
        return self.is_staff

    def has_perm(self, perm: str, obj: object = None) -> bool:
        """Needed for the admin part."""
        return self.is_staff

    def has_security_key(self) -> bool:
        """Check if the user has added a TOTP to their account."""
        return TOTPDevice.objects.filter(user_id=self.id).exists()

    def check_security_key(self, security_key: str) -> bool:
        """Check if a given code is correct."""
        return not self.has_security_key() or verify_token(
            self,
            TOTPDevice.objects.get(user_id=self.id).persistent_id,
            security_key,
        )

    def check_credentials(self, password: str, security_key: str) -> bool:
        """Check if a password as well as a code are correct."""
        return self.check_password(password) and self.check_security_key(security_key)

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

    def natural_key(self) -> tuple[str, ...]:
        """Create a natural key."""
        return (self.email,)

    def __str__(self) -> str:
        """Represent the class objects as a string."""
        return f"{self.email}"
