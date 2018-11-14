from django.views import generic

from packages.models import Package


class IndexView(generic.TemplateView):
    template_name = 'home/index.html'
    context_object_name = 'latest_packages'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'keyword_links': True,
            'package_links': True,
            # Get the last five published packages.
            'latest_packages': Package.objects.order_by('-date_created')[:5],
        })

        return context
