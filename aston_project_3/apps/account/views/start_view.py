"""The starting view."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View


class StartViewSet(View):
    """The starting view."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """GET method."""
        if request.user.is_authenticated:
            return redirect("account:home")
        else:
            return render(request, "home/start.html")
