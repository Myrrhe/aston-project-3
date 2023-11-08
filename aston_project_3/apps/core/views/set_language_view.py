"""The language view"""
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import resolve, Resolver404, reverse
from django.utils.translation import (
    activate,
    check_for_language,
    get_language_from_path,
)
from django.utils import translation
from django.views import View
from django.urls import get_resolver
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import translate_url


class SetLanguageViewSet(View):
    """The language view"""

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        """
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
            url = current_url
            response = HttpResponseRedirect(url)
            if "language" in request.POST:
                response["Accept-Language"] = request.POST["language"]
                url_splitted = url.split("/")
                url_splitted[1] = request.POST["language"]
                response = HttpResponseRedirect("/".join(url_splitted))
                activate(request.POST["language"])
            return response
        else:
            url = reverse("empty")
            response = HttpResponseRedirect(url)
            return response
        """
        next_url = request.POST.get("next", request.GET.get("next"))
        if (
            next_url or request.accepts("text/html")
        ) and not url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            next_url = request.META.get("HTTP_REFERER")
            if not url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                next_url = "/"
        response = (
            HttpResponseRedirect(next_url) if next_url else HttpResponse(status=204)
        )
        if request.method == "POST":
            lang_code = request.POST.get("language")
            if lang_code and check_for_language(lang_code):
                activate(get_language_from_path(next_url))
                if next_url:
                    url_is_allowed = None
                    try:
                        resolve(next_url)
                        url_is_allowed = True
                    except Resolver404:
                        url_is_allowed = False
                    if url_is_allowed:
                        next_url = reverse(resolve(next_url).url_name)
                        url_splitted = next_url.split("/")
                        url_splitted[1] = lang_code
                        next_trans = "/".join(url_splitted)
                        if next_trans != next_url:
                            response = HttpResponseRedirect(next_trans)
                    else:
                        response = HttpResponseRedirect("/")
                response["Accept-Language"] = lang_code
                activate(lang_code)
                # response.set_cookie(
                #     settings.LANGUAGE_COOKIE_NAME,
                #     lang_code,
                #     max_age=settings.LANGUAGE_COOKIE_AGE,
                #     path=settings.LANGUAGE_COOKIE_PATH,
                #     domain=settings.LANGUAGE_COOKIE_DOMAIN,
                #     secure=settings.LANGUAGE_COOKIE_SECURE,
                #     httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
                #     samesite=settings.LANGUAGE_COOKIE_SAMESITE,
                # )
        return response
