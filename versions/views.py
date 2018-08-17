from django.views import generic

from .models import Version


class IndexView(generic.ListView):
    template_name = 'versions/index.html'
    context_object_name = 'version_dicts'

    def get_queryset(self):
        versions = Version.objects.order_by('-date_created')

        return list(map(lambda x: {
            'author': x.author,
            'version': x,
            'parent_package': x.parent_package
        }, versions))


class DetailView(generic.DetailView):
    template_name = 'versions/detail.html'
    model = Version
    context_object_name = 'version_dict'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        version = data['version_dict']
        data['version_dict'] = {
            'author': version.author,
            'parent_package': version.parent_package,
            'version': version,
        }

        return data
