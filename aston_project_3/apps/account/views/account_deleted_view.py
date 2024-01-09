"""The account deleted view."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class AccountDeletedViewSet(View):
    """The account deleted view."""

    template_name = "account/deleted.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """GET method."""
        return render(request, self.template_name)
