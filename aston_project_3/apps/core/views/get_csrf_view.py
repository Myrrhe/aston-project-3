"""The CSRF token getter view."""
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.middleware.csrf import get_token
from django.views import View


class GetCSRFViewSet(View):
    """The CSRF token getter view."""

    def get(
        self,
        request: HttpRequest
    ) -> HttpResponseRedirect:
        """GET method."""
        csrf_token = get_token(request)
        return JsonResponse({'csrf_token': csrf_token})
