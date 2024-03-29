"""The view where the user is redirected after having created their account."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View


class AccountCreatedViewSet(View):
    """The account creation report view."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """GET method."""
        if request.user.is_authenticated:
            return redirect("account:home")
        return render(request, "registration/account_created.html")
