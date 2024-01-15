"""The cookies settings view."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class CookiesSettingsViewSet(View):
    """The cookies settings view."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """GET method."""
        return render(request, "cookies/settings.html")
