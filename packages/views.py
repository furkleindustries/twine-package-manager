import requests

from os import path
from urllib.parse import urlparse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .forms import PackageCreateForm, PackageUpdateForm
from packages.models import Package, PackageDownload
from packages.search import packages_search_filter
from versions.models import Version

from .models import Package


class IndexView(generic.TemplateView):
    template_name = 'packages/index.html'
    context_object_name = 'packages'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        fetch_params = {
            'page_size': self.request.GET.get('page_size') or 1,
            'cursor': self.request.GET.get('cursor') or '',
        }

        url = self.request.build_absolute_uri('/api/packages/')

        fetched = requests.get(url, fetch_params)
        obj = fetched.json()
        packages = obj['results']
        previous_url = (obj['previous'] or '').replace('/api', '')
        next_url = (obj['next'] or '').replace('/api', '')

        context.update({
            'keyword_links': True,
            'packages': packages,
            'package_links': True,
            'package_small_size': True,
            'previous_url': previous_url,
            'next_url': next_url,
        })

        return context


class KeywordView(generic.ListView):
    template_name = 'packages/keywords.html'
    context_object_name = 'packages'

    def get_queryset(self):
        packages = Package.objects.all()
        keyword = self.kwargs['keyword']
        return packages.filter(keywords__icontains=keyword).order_by(
            'packagedownload'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'as_list': True,
            'keyword': self.kwargs.get('keyword') or '',
            'keyword_links': True,
        })

        return context


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
            'as_list': True,
            'keyword_links': True,
            'query': self.request.GET.get('query') or '',
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
        versions = package.version_set.all()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package = None
        unique_field = self.kwargs['unique_field']
        if unique_field.isdigit():
            package = Package.objects.get(id=unique_field)
        else:
            package = Package.objects.get(name=unique_field)

        versions = list(Version.objects.filter(parent_package=package))
        versions.sort(
            # Sort them as lists of major-minor-patch versions, in (hopefully)
            # valid semver order.
            key=lambda x: x.version_identifier.split('.'),
            reverse=True,
        )

        back_url = '/packages/{}/edit/'.format(unique_field)

        context.update({
            'package': package,
            'form_after_submit_redirect': back_url,
            'form_destination': '/api/versions/',
            'form_method': 'POST',
            'form_selector': '#versionCreate',
            'existing_versions': versions,
        })

        return context
