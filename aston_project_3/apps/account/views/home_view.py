"""The home view."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View


class HomeViewSet(View):
    """The home view."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """GET method."""
        if request.user.is_authenticated:
            return render(request, "home/home.html")
        return redirect("account:login", "")
