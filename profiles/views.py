from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views import generic

from packages.models import Package
from .models import Profile


class DetailView(generic.DetailView):
    model = User
    template_name = 'profiles/detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = context.get('user')

        context['packages'] = Package.objects.filter(owner_id=user.id)
        context['profile'] = user.profile
        context['with_labels'] = True
        context['with_dates'] = True
        return context
