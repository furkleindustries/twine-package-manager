from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView


class TpmLogoutView(LoginRequiredMixin, LogoutView):
    pass
