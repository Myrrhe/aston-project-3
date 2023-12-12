"""The signup view."""
from django.urls import reverse_lazy
from django.views import generic

from apps.account.forms import SignupForm


class SignupViewSet(generic.CreateView):
    """The signup view."""

    template_name = "registration/signup.html"
    form_class = SignupForm
    success_message = "Your profile was created successfully"

    def get_success_url(self) -> any:
        """Determine where the user is redirected on success."""
        return reverse_lazy(
            "account:account-created",
        )
