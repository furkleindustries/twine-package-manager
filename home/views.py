from django.views import generic

from packages.models import Package


class IndexView(generic.TemplateView):
    template_name = 'home/index.html'
    context_object_name = 'latest_packages'

    def get_context_data(self, **kwargs):
        ''' Add the logged_in variable to the context.
        '''
        context = super().get_context_data(**kwargs)
        context['keyword_links'] = True
        context['logged_in'] = self.request.user.is_authenticated
        context['package_links'] = True

        # Get the last five published packages.
        latest_packages = Package.objects.order_by('-date_created')[:5]
        context['latest_packages'] = latest_packages

        return context
