"""The home view"""
from django.http import HttpRequest, HttpResponse
from django.views import View


class HomeViewSet(View):
    """The home view"""

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return HttpResponse("Hello, World!")
