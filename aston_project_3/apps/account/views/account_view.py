"""The account view."""
from django.contrib.auth import update_session_auth_hash
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from apps.account.forms import (
    ChangeEmailForm,
    ChangePasswordForm,
    PersonalInformationsForm,
)
from apps.core.utils.get_form_util import get_form


class AccountViewSet(View):
    """The account view."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """GET method."""
        if request.user.is_authenticated:
            return render(
                request,
                "account/account.html",
                context={
                    "email_form": ChangeEmailForm(
                        prefix="email_form",
                        user=request.user,
                    ),
                    "password_form": ChangePasswordForm(
                        prefix="password_form",
                        user=request.user,
                    ),
                    "personal_informations_form": PersonalInformationsForm(
                        prefix="personal_informations_form",
                        initial={
                            "username": request.user.username,
                            "biography": request.user.biography,
                        },
                    ),
                    "has_security_key": request.user.has_security_key(),
                },
            )
        else:
            return redirect("account:login", "")

    def post(self, request: HttpRequest) -> HttpResponse:
        """POST method."""
        change_email_form = get_form(
            request, ChangeEmailForm, "email_form", user=request.user
        )
        change_password_form = get_form(
            request, ChangePasswordForm, "password_form", user=request.user
        )
        personnal_informations_form = get_form(
            request, PersonalInformationsForm, "personal_informations_form"
        )
        if change_email_form.is_bound and change_email_form.is_valid():
            # Email
            change_email_form.save(request)
            update_session_auth_hash(request, request.user)
        if change_password_form.is_bound and change_password_form.is_valid():
            # Password
            change_password_form.save(request)
            update_session_auth_hash(request, request.user)
        if (
            personnal_informations_form.is_bound
            and personnal_informations_form.is_valid()
        ):
            # Personal informations
            personnal_informations_form.save(request)
        return render(
            request,
            "account/account.html",
            context={
                "email_form": change_email_form,
                "password_form": change_password_form,
                "personal_informations_form": personnal_informations_form,
                "has_security_key": request.user.has_security_key(),
            },
        )
