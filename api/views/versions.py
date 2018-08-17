from json import loads

from .api_responses import *

from versions.models import Version


def versions(request, version_id):
    method = request.method

    if method == 'POST':
        user = request.user
        post = loads(request.body)

        if not user.is_authenticated:
            return get_permission_denied_response('version', method)

        version = Version.objects.get(id=version_id)
        if not version:
            return get_item_not_found_response('version', version_id)
        elif version.author_id != user.id:
            return get_item_not_owned_response('version', version_id)
        # Fill in version creation here.

    # Requires version_id pretty url argument
    if method == 'GET' or method == 'DELETE':
        if not version_id:
            return get_id_not_provided_response('version', method)

        if method == 'GET':
            try:
                return get_item_response(Version.objects.get(id=version_id))
            except Version.DoesNotExist:
                return get_item_not_found_response('version', version_id)
        # There is no PUT method for versions as they are immutable.
        elif method == 'DELETE':
            if not request.user.is_authenticated:
                return get_permission_denied_response('version', method)

            version = Version.objects.get(id=version_id)
            if not version:
                return get_item_not_found_response('version', version_id)
            elif version.author_id != request.user.id:
                return get_item_not_owned_response('version', version_id)
            # Fill in version deletion here.

    return get_method_not_supported_response('version', method)
