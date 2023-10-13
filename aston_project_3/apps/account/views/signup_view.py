"""The signup view"""
from django.urls import reverse_lazy
from apps.account.forms import SignupForm
from django.views import generic


class SignupViewSet(generic.CreateView):
    """The signup view"""

    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    form_class = SignupForm
    success_message = "Your profile was created successfully"
