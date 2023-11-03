"""The account view"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View


class AccountViewSet(View):
    """The account view"""

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return render(request, "account/account.html")
        else:
            return redirect("login", "")
