from django.views import generic
from django.shortcuts import render

from .models import Profile
from packages.models import Package
from versions.models import Version


class IndexView(generic.TemplateView):
    template_name = 'profiles/index.html'


class DetailView(generic.DetailView):
    template_name = 'profiles/detail.html'
    model = Profile

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        profile = data['object']
        packages = Package.objects.filter(owner=profile.user)
        return {
            'packages': packages,
            'profile': profile,
        }
