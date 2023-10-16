"""The home view"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views import View


class HomeViewSet(View):
    """The home view"""

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return HttpResponse("Hello, World!")
        else:
            return redirect("login")
