from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views import generic

from packages.models import Package
from .models import Profile


def trim_profile(profile: Profile):
    # Only include 140 characters of description.
    trimmed_description = profile.description[0:140].strip()
    if len(trimmed_description) == 140:
        trimmed_description = '{}{}'.format(trimmed_description, '...')

    return {
        'description': trimmed_description,
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
        temp.sort(key=lambda profile: profile.user.date_joined, reverse=True)
        trimmed = list(map(trim_profile, temp))
        return trimmed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logged_in'] = self.request.user.is_authenticated
        context['with_links'] = True
        return context


class DetailView(generic.DetailView):
    model = User
    template_name = 'profiles/detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context.get('user')
        context['logged_in'] = user.is_authenticated
        context['packages'] = Package.objects.filter(owner_id=user.id)
        context['profile'] = user.profile
        context['with_labels'] = True
        context['with_dates'] = True
        return context
