from json import loads

from packages.models import Package

from .api_responses import *


def packages(request, package_id):
    method = request.method

    if method == 'POST':
        user = request.user
        post = loads(request.body)

        if not user.is_authenticated:
            return get_permission_denied_response('package', method)

        name = post.get('name')
        description = post.get('description')
        homepage = post.get('homepage') or ''
        tag = post.get('tag') or ''

        if not name:
            return get_argument_not_provided_response('package', 'name',
                                                      'creating')

        already_exists_package = None
        try:
            already_exists_package = Package.objects.get(name=name)
        except Package.DoesNotExist:
            pass

        if already_exists_package:
            return get_name_already_exists_response('package', name)
        elif not description:
            return get_argument_not_provided_response('package', 'description',
                                                      'creating')

        package = Package.objects.create(
            author=user,
            description=description,
            homepage=homepage,
            name=name,
            owner=user,
            tag=tag,
        )

        return get_item_response(package)

    # Requires package_id pretty url argument
    if method == 'GET' or method == 'PUT' or method == 'DELETE':
        if not package_id:
            return get_id_not_provided_response('package', method)

        if method == 'GET':
            try:
                return get_item_response(Package.objects.get(id=package_id))
            except Package.DoesNotExist:
                return get_item_not_found_response('package', package_id)
        elif method == 'PUT':
            if not request.user.is_authenticated:
                return get_permission_denied_response('package', method)

            package = Package.objects.get(id=package_id)
            if not package:
                return get_item_not_found_response('package', package_id)
            elif package.author_id != request.user.id:
                return get_item_not_owned_response('package', package_id)
            # Fill in package updating here.
        elif method == 'DELETE':
            if not request.user.is_authenticated:
                return get_permission_denied_response('package', method)

            package = Package.objects.get(id=package_id)
            if not package:
                return get_item_not_found_response('package', package_id)
            elif package.author_id != request.user.id:
                return get_item_not_owned_response('package', package_id)
            # Fill in version deletion here.

    return get_method_not_supported_response('package', method)
