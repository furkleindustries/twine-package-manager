from django.contrib.auth.views import LoginView


class TpmLoginView(LoginView):
    template_name = 'login/index.html'
    redirect_authenticated_user = True
