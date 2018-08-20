from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from packages.models import Package
from versions.models import Version

from .models import Package


class IndexView(generic.ListView):
    template_name = 'packages/index.html'
    context_object_name = 'package_dicts'

    def get_queryset(self):
        packages = Package.objects.order_by('-date_created')
        return list(map(lambda x: {
            'author': x.author,
            'owner': x.owner,
            'package': x,
        }, packages))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logged_in'] = self.request.user.is_authenticated
        return context


class DetailView(generic.DetailView):
    template_name = 'packages/detail.html'
    context_object_name = 'package'
    model = Package

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package = context['package']
        context.update({
            'author':  package.author,
            'logged_in': self.request.user.is_authenticated,
            'package': package,
            'owner': package.owner,
            'versions': list(Version.objects.filter(parent_package=package))
        })

        return context


class UpdateView(LoginRequiredMixin, generic.DetailView):
    context_object_name = 'package'
    model = Package
    template_name = 'packages/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package = context['package']
        versions = Version.objects.filter(parent_package=package)
        versions = versions.order_by('-date_created')
        context['form_after_submit_action'] = 'update_page'
        context['form_destination'] = '/api/packages/{}/'.format(package.id)
        context['form_method'] = 'PUT'
        context['form_selector'] = '#packageUpdate'
        context['logged_in'] = True
        context['versions'] = versions
        return context


class CreateView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'packages/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_destination'] = '/api/packages/'
        context['form_method'] = 'POST'
        context['form_selector'] = '#packageCreate'
        context['logged_in'] = True
        return context


class DeleteView(LoginRequiredMixin, generic.DeleteView):
    context_object_name = 'package'
    model = Package
    template_name = 'packages/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package = context['package']
        versions = list(Version.objects.filter(parent_package=package))
        context['form_destination'] = '/api/packages/{}/'.format(package.id)
        context['form_method'] = 'DELETE'
        context['form_selector'] = '#packageDelete'
        context['logged_in'] = True
        context['versions'] = versions
        return context


class CreateVersionView(LoginRequiredMixin, generic.TemplateView):
    model = Version
    template_name = 'packages/create_version.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_id = self.kwargs['pk']
        package = Package.objects.get(id=package_id)
        context['package'] = package
        versions = list(Version.objects.filter(parent_package=package))
        context['form_destination'] = '/api/versions/'
        context['form_method'] = 'POST'
        context['form_selector'] = '#versionCreate'
        context['logged_in'] = True
        context['existing_versions'] = versions
        return context
