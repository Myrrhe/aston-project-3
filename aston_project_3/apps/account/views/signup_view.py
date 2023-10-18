"""The signup view"""
from django.urls import reverse, reverse_lazy
from apps.account.forms import SignupForm
from django.views import generic


class SignupViewSet(generic.CreateView):
    """The signup view"""

    template_name = "registration/signup.html"
    form_class = SignupForm
    success_message = "Your profile was created successfully"

    def get_success_url(self) -> any:
        return reverse_lazy(
            "account-created",
        )
