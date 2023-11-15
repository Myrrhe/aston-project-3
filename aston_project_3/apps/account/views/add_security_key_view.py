"""The security key creation view"""
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from apps.account.forms import CreateSecurityKeyForm
from django_otp.plugins.otp_totp.models import TOTPDevice


class AddSecurityKeyViewSet(CreateView):
    """The security key creation view"""

    model = TOTPDevice
    form_class = CreateSecurityKeyForm
    template_name = "security_key/add.html"

    def get_success_url(self) -> any:
        return reverse_lazy(
            "account:add-security-key",
        )

    def get_context_data(self, **kwargs) -> any:
        context = super().get_context_data(**kwargs)
        context["has_security_key"] = self.request.user.has_security_key()
        return context

    def get_form_kwargs(self) -> any:
        """Passes the request object to the form class.
        This is necessary to give the current user to the form"""
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    # def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
    #     return render(
    #         request,
    #         "security_key/add.html",
    #         context={
    #             "security_key_form": CreateSecurityKeyForm(
    #                 {"new_code": b32encode(totp.bin_key).decode("utf-8")}
    #             )
    #         },
    #     )

    # def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
    #     security_key_form = CreateSecurityKeyForm(request.POST)
    #     if security_key_form.is_bound and security_key_form.is_valid():
    #         security_key_form.save(request)
    #     else:
    #         pass
    #     return redirect("account:add-security-key")
