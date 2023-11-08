"""The view where the user is redirected after having created their account"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View


class AccountCreatedViewSet(View):
    """The account creation report view"""

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("account:home")
        else:
            return render(request, "registration/account_created.html")
