from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views import generic

from packages.models import Package
from .models import Profile


def trim_profile(profile: Profile):
    trimmed_description = profile.description[0:140].strip()
    return {
        # Only include 140 characters of description.
        'description': '%s%s' % (trimmed_description, '...'),
        'user': {
            'username': profile.user.username,
        },
        'user_id': profile.user_id,
    }


class IndexView(generic.ListView):
    template_name = 'profiles/index.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        temp = list(Profile.objects.all())
        temp.sort(key=lambda x: x.user.date_joined, reverse=True)
        trimmed = list(map(trim_profile, temp))
        return trimmed


class DetailView(generic.DetailView):
    model = User
    template_name = 'profiles/detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        user = context.get('user')
        context['logged_in'] = user.is_authenticated
        context['packages'] = Package.objects.filter(owner_id=user.id)
        context['profile'] = user.profile
        return context
