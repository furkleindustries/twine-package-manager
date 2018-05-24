from json import dumps

from django.forms.models import model_to_dict
from django.http import HttpResponse

from packages.models import Package
from profiles.models import Profile
from versions.models import Version


def get_method_not_recognized_response(method):
    response = HttpResponse(
        dumps({
            'error': 'The request method, %s, was not recognized.' % method
        }),
        status=500,
    )

    response['Content-type'] = 'application/json'
    return response


def get_item_not_found_response(_type, _id):
    response = HttpResponse(
        dumps({
            'error': 'There was no %s found with id %s.' % (_type, _id)
        }),
        status=404
    )

    response['Content-type'] = 'application/json'
    return response


def item_response(item):
    response = HttpResponse(
        dumps(model_to_dict(item))
    )

    response['Content-type'] = 'application/json'
    return response


def packages(request, package_id):
    method = request.method
    if method == 'GET':
        try:
            return item_response(Package.objects.get(id=package_id))
        except Package.DoesNotExist:
            return get_item_not_found_response('package', package_id)
    elif method == 'POST':
        pass
    elif method == 'PUT':
        pass
    elif method == 'DELETE':
        pass
    elif method == 'OPTIONS':
        pass

    return get_method_not_recognized_response(method)


def profiles(request, profile_id):
    method = request.method
    if method == 'GET':
        try:
            return item_response(Profile.objects.get(user_id=profile_id))
        except Profile.DoesNotExist:
            return get_item_not_found_response('profile', profile_id)
    elif method == 'POST':
        pass
    elif method == 'PUT':
        pass
    elif method == 'DELETE':
        pass
    elif method == 'OPTIONS':
        pass

    return get_method_not_recognized_response(method)


def versions(request, version_id):
    method = request.method
    if method == 'GET':
        try:
            return item_response(Version.objects.get(id=version_id))
        except Version.DoesNotExist:
            return get_item_not_found_response('version', version_id)
    elif method == 'POST':
        pass
    # There is no PUT method for versions as they are immutable.
    elif method == 'DELETE':
        pass
    elif method == 'OPTIONS':
        pass

    return get_method_not_recognized_response(method)