from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from packages.models import Package
from profiles.models import Profile


class AccountView(LoginRequiredMixin, generic.TemplateView):
    model = Profile
    template_name = 'account/index.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context.update({
            'form_after_submit_action': 'update_page',
            'form_destination': '/api/profiles/{}/'.format(user.id),
            'form_method': 'PUT',
            'form_selector': '#accountUpdate',
            'packages': Package.objects.filter(author_id=user.id).order_by(
                '-date_created'),
            'profile': get_object_or_404(Profile, user_id=user.id),
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
