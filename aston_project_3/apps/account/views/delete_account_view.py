"""The account deletion view"""
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from apps.account.forms import DeleteAccountForm
from apps.account.models import User


class DeleteAccountViewSet(FormView):
    """The account deletion view"""

    model = User
    form_class = DeleteAccountForm
    template_name = "account/delete.html"

    def get_success_url(self) -> any:
        return reverse_lazy(
            "account:account-deleted",
        )

    def get_context_data(self, **kwargs) -> any:
        context = super(DeleteAccountViewSet, self).get_context_data(**kwargs)
        context["has_security_key"] = self.request.user.has_security_key()
        return context

    def get_form_kwargs(self) -> any:
        kwargs = super(DeleteAccountViewSet, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs
