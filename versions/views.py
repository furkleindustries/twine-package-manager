from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import Version


class DetailView(generic.DetailView):
    model = Version
    context_object_name = 'version'
    template_name = 'versions/detail.html'
