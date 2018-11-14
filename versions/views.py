from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import Version


class IndexView(generic.ListView):
    template_name = 'versions/index.html'
    context_object_name = 'versions'

    def get_queryset(self):
        return Version.objects.order_by('-date_created')


class DetailView(generic.DetailView):
    template_name = 'versions/detail.html'
    model = Version
    context_object_name = 'version'
