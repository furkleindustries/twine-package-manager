from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, render

from packages.models import Package
from profiles.models import Profile


@login_required
def account(request):
    user = request.user
    packages = Package.objects.filter(author_id=user.id)
    profile = get_object_or_404(Profile, user_id=user.id)

    return render(request, 'account/index.html', {
        'logged_in': True,
        'packages': packages,
        'profile': profile,
        'user': user,
    })
