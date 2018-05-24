from django.shortcuts import render

from .models import Profile
from packages.models import Package


def detail(request, profile_id):
    profile = None
    try:
        profile = Profile.objects.get(user_id=profile_id)
    except Profile.DoesNotExist:
        pass

    packages = Package.objects.filter(owner_id=profile_id)
    
    context = {
        'packages': packages,
        'profile': profile,
    }

    return render(request, 'profiles/detail.html', context)
