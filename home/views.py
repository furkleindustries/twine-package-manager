from django.views import generic

from packages.models import Package


class IndexView(generic.ListView):
    template_name = 'home/index.html'
    context_object_name = 'latest_package_dicts'

    def get_queryset(self):
        '''Return the last five published packages.'''
        packages = Package.objects.order_by('-date_created')[:5]
        return list(map(lambda x: {
            'author': x.author,
            'package': x,
            'owner': x.owner,
        }, packages))

    def get_context_data(self, **kwargs):
        ''' Add the logged_in variable to the context.
        '''
        context = super().get_context_data(**kwargs)
        context['logged_in'] = self.request.user.is_authenticated
        return context
