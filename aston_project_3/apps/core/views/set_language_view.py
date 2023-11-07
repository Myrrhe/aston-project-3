"""The language view"""
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.translation import activate
from django.views import View


class SetLanguageViewSet(View):
    """The language view"""

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        response = HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        if "language" in request.POST:
            activate(request.POST["language"])
            response["Accept-Language"] = request.POST["language"]
            url_splitted = request.META.get("HTTP_REFERER").split("/")
            url_splitted[3] = request.POST["language"]
            response = HttpResponseRedirect("/".join(url_splitted))
        return response
