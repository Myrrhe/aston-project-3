"""The security key creation view"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class AddSecurityKeyViewSet(View):
    """The security key creation view"""

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, "security_key/add.html")
