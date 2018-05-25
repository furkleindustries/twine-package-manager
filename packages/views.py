from django.shortcuts import render
from django.views import generic

from packages.models import Package
from versions.models import Version

from .models import Package


class IndexView(generic.ListView):
    template_name = 'packages/index.html'
    context_object_name = 'latest_package_dicts'

    def get_queryset(self):
        packages = Package.objects.order_by('-date_created')
        return list(map(lambda x: {
            'package': x,
            'author': x.author,
            'owner': x.owner,
        }, packages))


class DetailView(generic.DetailView):
    template_name = 'packages/detail.html'
    context_object_name = 'package_dict'
    model = Package

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        package = data['package_dict']
        data['package_dict'] = {
            'author':  package.author,
            'package': package,
            'owner': package.owner,
            'versions': list(Version.objects.filter(parent_package=package))
        }

        return data
