from django.http import HttpResponse
from django.views import generic

from packages.models import Package


class IndexView(generic.ListView):
    template_name = 'home/index.html'
    context_object_name = 'latest_package_dicts'

    def get_queryset(self):
        '''Return the last five published questions.'''
        packages = Package.objects.order_by('-date_created')[:5]
        return list(map(lambda x: {
            'package': x,
            'author': x.author,
            'owner': x.owner,
        }, packages))
