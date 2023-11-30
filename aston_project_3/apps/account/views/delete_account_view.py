"""The account deletion view."""
from django.forms import Form
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from apps.account.forms import DeleteAccountForm
from apps.account.models import User


class DeleteAccountViewSet(FormView):
    """The account deletion view."""

    model = User
    form_class = DeleteAccountForm
    template_name = "account/delete.html"

    def get_success_url(self) -> any:
        """Determine where the user is redirected on success."""
        return reverse_lazy(
            "account:account-deleted",
        )

    def form_valid(self, form: Form) -> HttpResponse:
        """Trigger an action when the submitted form is valid."""
        form.delete_account()
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> any:
        """Send additionnal data to the template."""
        context = super().get_context_data(**kwargs)
        context["has_security_key"] = self.request.user.has_security_key()
        return context

    def get_form_kwargs(self) -> any:
        """
        Pass the request object to the form class.

        This is necessary to give the current user to the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
