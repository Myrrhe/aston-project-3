"""The language view"""
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import resolve, Resolver404, reverse
from django.utils.translation import activate, get_language_from_path
from django.utils import translation
from django.views import View
from django.urls import get_resolver
from django.contrib.sites.shortcuts import get_current_site


class SetLanguageViewSet(View):
    """The language view"""

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        current_url = (
            request.META.get("HTTP_REFERER")
            .replace("http://", "")
            .replace(request.META.get("HTTP_HOST"), "")
        )

        activate(get_language_from_path(current_url))

        url_is_allowed = False
        try:
            resolve(current_url)
            url_is_allowed = True
        except Resolver404:
            url_is_allowed = False

        url = ""
        if url_is_allowed:
            url = request.META.get("HTTP_REFERER")
            response = HttpResponseRedirect(url)
            if "language" in request.POST:
                response["Accept-Language"] = request.POST["language"]
                url_splitted = url.split("/")
                url_splitted[3] = request.POST["language"]
                response = HttpResponseRedirect("/".join(url_splitted))
                activate(request.POST["language"])
            return response
        else:
            url = reverse("empty")
            response = HttpResponseRedirect(url)
            return response
