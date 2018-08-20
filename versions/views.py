from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import Version


class IndexView(generic.ListView):
    template_name = 'versions/index.html'
    context_object_name = 'versions'

    def get_queryset(self):
        return Version.objects.order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'logged_in': self.request.user.is_authenticated,
        })

        return context


class DetailView(generic.DetailView):
    template_name = 'versions/detail.html'
    model = Version
    context_object_name = 'version'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'logged_in': self.request.user.is_authenticated,
        })

        return context


class UpdateView(LoginRequiredMixin, generic.DetailView):
    context_object_name = 'package'
    model = Version
    template_name = 'versions/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package = context['version']
        context['form_after_submit_action'] = 'update_page'
        context['form_destination'] = '/api/versions/{}/'.format(package.id)
        context['form_method'] = 'PUT'
        context['form_selector'] = '#versionUpdate'
        context['logged_in'] = True
        return context