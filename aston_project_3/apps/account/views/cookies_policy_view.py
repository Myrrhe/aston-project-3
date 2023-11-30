"""The cookies policy view."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class CookiesPolicyViewSet(View):
    """The cookies policy view."""

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """GET method."""
        return render(request, "cookies/policy.html")
