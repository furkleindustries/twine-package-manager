from django.shortcuts import render

from profiles.models import Profile
from versions.models import Version
from .models import Package


def detail(request, package_id):
    package = None
    try:
        package = Package.objects.get(id=package_id)
    except Package.DoesNotExist:
        pass

    author = None
    try:
        author = Profile.objects.get(user_id=package.author)
    except Profile.DoesNotExist:
        pass

    owner = None
    try:
        owner = Profile.objects.get(user_id=package.owner)
    except Profile.DoesNotExist:
        pass

    versions = Version.objects.filter(parent_package_id=package_id)

    context = {
        'author': author,
        'owner': owner,
        'package': package,
        'versions': versions,
    }

    return render(request, 'packages/detail.html', context)
