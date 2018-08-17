from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class TpmLoginView(LoginView):
    template_name = 'login/index.html'
    redirect_authenticated_user = True

    def get_redirect_field_name(self):
        return None

    def get_context_data(self, **kwargs):
        ''' Add the logged_in variable to the context.
        '''
        context = super().get_context_data(**kwargs)
        return context
