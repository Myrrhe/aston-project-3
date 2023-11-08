"""The account view"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from apps.account.forms import ChangeEmailForm
from apps.core.utils.get_form_util import get_form
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp import verify_token


class AccountViewSet(View):
    """The account view"""

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return render(
                request,
                "account/account.html",
                context={"email_form": ChangeEmailForm(prefix="email_form")},
            )
        else:
            return redirect("account:login", "")

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        change_email_form = get_form(request, ChangeEmailForm, "email_form")
        if change_email_form.is_bound and change_email_form.is_valid():
            credentials_ok = None
            if request.user.check_password(change_email_form.cleaned_data["password"]):
                if TOTPDevice.objects.filter(user_id=request.user.id).exists():
                    if verify_token(
                        request.user,
                        TOTPDevice.objects.get(user_id=request.user.id).persistent_id,
                        change_email_form.cleaned_data["security_key"],
                    ):
                        credentials_ok = True
                    else:
                        credentials_ok = False
                else:
                    credentials_ok = True
            else:
                credentials_ok = False
            if credentials_ok:
                change_email_form.save(request)
            else:
                pass
        return redirect("account:account")

    # def change_email(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
    #     if request.user.is_authenticated:
    #         if request.method == "POST":
    #             form = ChangeEmailForm(request.POST)
    #             if form.is_valid():
    #                 form.save()
    #                 return redirect("account:account")
    #         return []
    #     else:
    #         return redirect("account:login", "")
