from os import path
from urllib.parse import urlparse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from api.views import (
    PackageDetailRetrieveOnly,
    PackageKeywordList,
    PackageListOnly,
    PackageSearch,
)

from packages.models import Package, PackageDownload
from packages.search import packages_search_filter
from versions.models import Version

from .forms import PackageCreateForm, PackageUpdateForm
from .models import Package
from .renderers import (
    PackageAuthorAndOwnerAwareTemplateHTMLRenderer,
    PackageOwnerAwareTemplateHTMLRenderer,
)


class IndexView(PackageListOnly):
    renderer_classes = (PackageOwnerAwareTemplateHTMLRenderer,)
    template_name = 'packages/index.html'

    def get_renderer_context(self):
        context = super().get_renderer_context()

        ordering_field = self.request.GET.get('ordering')

        ordering_direction = 'ascending'
        if not ordering_field:
            ordering_direction = 'descending'
        elif ordering_field[0] == '-':
            ordering_field = ordering_field[1:]
            ordering_direction = 'descending'

        context.update({
            'as_list': True,
            'keyword_links': True,
            'ordering_direction': ordering_direction,
            'ordering_field': ordering_field,
            'package_links': True,
            'show_owner': True,
        })

        return context


class KeywordView(PackageKeywordList):
    renderer_classes = (PackageOwnerAwareTemplateHTMLRenderer,)
    template_name = 'packages/keywords.html'

    def get_renderer_context(self):
        context = super().get_renderer_context()
        context.update({
            'as_list': True,
            'keyword': self.kwargs.get('keyword') or '',
            'keyword_links': True,
            'package_links': True,
            'show_author': True,
        })

        return context


class SearchView(PackageSearch):
    renderer_classes = (PackageOwnerAwareTemplateHTMLRenderer,)
    template_name = 'packages/search.html'

    def get_renderer_context(self):
        context = super().get_renderer_context()
        context.update({
            'as_list': True,
            'keyword_links': True,
            'package_links': True,
            'query': self.request.GET.get('query') or '',
            'show_author': True,
        })

        return context


class DetailView(PackageDetailRetrieveOnly):
    renderer_classes = (PackageAuthorAndOwnerAwareTemplateHTMLRenderer,)
    template_name = 'packages/detail.html'

    def get_renderer_context(self):
        context = super().get_renderer_context()
        print(self.request.user)
        context.update({
            'keyword_links': True,
            'show_author': True,
            'show_downloads': True,
            'show_labels': True,
            'show_owner': True,
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
            'form': PackageCreateForm,
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
            key=lambda x: x.semver_identifier.split('.'),
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
