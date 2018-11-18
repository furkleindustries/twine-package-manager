from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .forms import PackageCreateForm, PackageUpdateForm
from packages.models import Package, PackageDownload
from packages.search import packages_search_filter
from versions.models import Version

from .models import Package


class IndexView(generic.ListView):
    template_name = 'packages/index.html'
    context_object_name = 'packages'

    def get_queryset(self):
        return Package.objects.order_by('-date_created')


class SearchView(generic.ListView):
    template_name = 'packages/search.html'
    context_object_name = 'packages'

    def get_queryset(self):
        packages = Package.objects.all()
        search = self.request.GET.get('query')
        if not search:
            return []

        search = search.strip()
        if search == '*':
            return packages

        return packages_search_filter(search, packages)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'query': self.request.GET.get('query'),
        })

        return context


class DetailView(generic.DetailView):
    template_name = 'packages/detail.html'
    context_object_name = 'package'

    def get_object(self):
        unique_field = self.kwargs['unique_field']
        if unique_field.isdigit():
            return Package.objects.get(id=unique_field)

        return Package.objects.get(name=unique_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package = context['package']
        downloads = package.packagedownload_set.count()
        versions = package.version_set
        default_version = None
        for version in versions:
            if version == package.default_version:
                default_version = version

        context.update({
            'package': package,
            'default_version': default_version,
            'downloads': downloads,
            'show_author': True,
            'show_labels': True,
            'show_downloads': True,
            'versions': versions,
        })

        return context


class UpdateView(LoginRequiredMixin, generic.UpdateView):
    context_object_name = 'package'
    template_name = 'packages/edit.html'
    model = Package
    form_class = PackageUpdateForm

    def get_object(self):
        unique_field = self.kwargs['unique_field']
        if unique_field.isdigit():
            return Package.objects.get(id=unique_field)

        return Package.objects.get(name=unique_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package = context['package']
        downloads = package.packagedownload_set.count()
        versions = package.version_set
        versions = versions.order_by('-date_created')
        context.update({
            'downloads': downloads,
            'versions': versions,
        })

        return context


class CreateView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'packages/create.html'

    def get_object(self):
        unique_field = self.kwargs['unique_field']
        if unique_field.isdigit():
            return Package.objects.get(id=unique_field)

        return Package.objects.get(name=unique_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_destination': '/api/packages/',
            'form_method': 'POST',
            'form_selector': '#packageCreate',
        })

        return context


class DeleteView(LoginRequiredMixin, generic.DeleteView):
    context_object_name = 'package'
    template_name = 'packages/delete.html'

    def get_object(self):
        unique_field = self.kwargs['unique_field']
        if unique_field.isdigit():
            return Package.objects.get(id=unique_field)

        return Package.objects.get(name=unique_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package = context['package']
        versions = list(Version.objects.filter(parent_package=package))
        context.update({
            'form_destination': '/api/packages/{}/'.format(package.id),
            'form_method': 'DELETE',
            'form_selector': '#packageDelete',
            'versions': versions,
        })

        return context


class CreateVersionView(LoginRequiredMixin, generic.TemplateView):
    model = Version
    template_name = 'packages/create_version.html'
    context_object_name = 'package'

    def get_object(self):
        unique_field = self.kwargs['unique_field']
        if unique_field.isdigit():
            return Package.objects.get(id=unique_field)

        return Package.objects.get(name=unique_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_name = self.kwargs['name']
        versions = list(Version.objects.filter(parent_package=package))
        versions.sort(
            # Sort them as lists of major-minor-patch versions, in (hopefully)
            # valid semver order.
            key=lambda x: x.version_identifier.split('.'),
            reverse=True,
        )

        back_url = '/packages/{}/edit/'.format(package_name)

        context.update({
            'package': package,
            'form_after_submit_redirect': back_url,
            'form_destination': '/api/versions/',
            'form_method': 'POST',
            'form_selector': '#versionCreate',
            'existing_versions': versions,
        })

        return context
