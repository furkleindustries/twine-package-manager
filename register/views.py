from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import generic


class IndexView(UserPassesTestMixin, generic.CreateView):
    form_class = UserCreationForm
    success_url = '/login/'
    template_name = 'register/index.html'

    def test_func(self):
        return not self.request.user.is_authenticated

    def get_login_url(self):
        return '/'

    def get_redirect_field_name(self):
        return None
