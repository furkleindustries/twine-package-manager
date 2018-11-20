from json import dumps

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import response
from django.shortcuts import redirect, render
from django.views import generic

from packages.models import Package
from profiles.models import Profile

from .forms import AccountUpdateForm, ProfileUpdateForm


class AccountView(LoginRequiredMixin, generic.TemplateView):
    model = Profile
    template_name = 'account/index.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        context = super().get_context_data(**kwargs)
        context.update({
            'account_form': AccountUpdateForm(instance=user),
            'profile_form': ProfileUpdateForm(instance=profile),
            'packages': Package.objects.filter(
                author_id=user.id
            ).order_by('-date_created'),

            'profile': profile,
            'user': user,
        })

        return context


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('/account/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'account/change_password.html', {
        'form': form,
    })
