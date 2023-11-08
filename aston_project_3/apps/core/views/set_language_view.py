"""The language view"""
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import resolve, Resolver404, reverse
from django.utils.translation import (
    activate,
    check_for_language,
    get_language_from_path,
)
from django.views import View
from django.utils.http import url_has_allowed_host_and_scheme


class SetLanguageViewSet(View):
    """The language view"""

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
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
        response = HttpResponseRedirect("/")
        if request.method == "POST":
            lang_code = request.POST.get("language")
            if lang_code and check_for_language(lang_code):
                activate(get_language_from_path(next_url))
                if next_url:
                    try:
                        resolved = resolve(next_url)
                        next_url = reverse(resolved.url_name, kwargs=resolved.kwargs)
                        url_splitted = next_url.split("/")
                        url_splitted[1] = lang_code
                        next_trans = "/".join(url_splitted)
                        if next_trans != next_url:
                            response = HttpResponseRedirect(next_trans)
                    except Resolver404:
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
