"""The signup form"""
from django import forms

from apps.account.models import User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    """The signup form"""

    email = forms.EmailField()

    class Meta(object):
        """The meta class"""

        model = User
        fields = ["email"]
