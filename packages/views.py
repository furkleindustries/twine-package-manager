from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from packages.models import Package
from versions.models import Version

from .models import Package


class IndexView(generic.ListView):
    template_name = 'packages/index.html'
    context_object_name = 'packages'

    def get_queryset(self):
        packages = Package.objects.order_by('-date_created')
        return packages

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
        versions = list(Version.objects.filter(parent_package=package))
        default_version = None
        for version in versions:
            if version == package.default_version:
                default_version = version

        context.update({
            'logged_in': self.request.user.is_authenticated,
            'package': package,
            'default_version': default_version,
            'versions': versions,
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
        context.update({
            'form_after_submit_action': 'update_page',
            'form_destination': '/api/packages/{}/'.format(package.id),
            'form_method': 'PUT',
            'form_selector': '#packageUpdate',
            'logged_in': True,
            'versions': versions,
        })

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
        context.update({
            'form_destination': '/api/packages/{}/'.format(package.id),
            'form_method': 'DELETE',
            'form_selector': '#packageDelete',
            'logged_in': True,
            'versions': versions,
        })

        return context


class CreateVersionView(LoginRequiredMixin, generic.TemplateView):
    model = Version
    template_name = 'packages/create_version.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_id = self.kwargs['pk']
        package = Package.objects.get(id=package_id)
        versions = list(Version.objects.filter(parent_package=package))
        versions.sort(
            # Sort them as lists of major-minor-patch versions, in (hopefully)
            # valid semver order.
            key=lambda x: list(map(int, x.version_identifier.split('.'))),
            reverse=True,
        )

        context.update({
            'package': package,
            'form_destination': '/api/versions/',
            'form_method': 'POST',
            'form_selector': '#versionCreate',
            'logged_in': True,
            'existing_versions': versions,
        })

        return context
