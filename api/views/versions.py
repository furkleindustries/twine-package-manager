from json import loads

from django.core.exceptions import ValidationError

from .api_responses import *

from packages.models import Package
from versions.models import Version


def versions(request, version_id):
    method = request.method

    if method == 'POST':
        user = request.user
        post = loads(request.body)

        if not user.is_authenticated:
            return get_permission_denied_response('version', method)

        if 'version_identifier' not in post:
            return get_argument_not_provided_response('version',
                                                      'version_identifier',
                                                      'creating')

        version_identifier = post['version_identifier']

        if 'package_id' not in post:
            return get_version_package_id_not_provided_response(
                version_identifier)

        package_id = post['package_id']
        package = None
        try:
            package = Package.objects.get(id=package_id)
        except Package.DoesNotExist:
            return get_item_not_found_response('package', package_id)

        if package.owner.id != user.id:
            return get_item_not_owned_response('package', package_id)

        existing_version = None
        try:
            existing_version = Version.objects.get(
                parent_package=package, version_identifier=version_identifier)
        except Version.DoesNotExist:
            pass

        if existing_version:
            return get_version_already_exists_response(package_id,
                                                       version_identifier)

        if 'description' not in post or not post['description']:
            return get_argument_not_provided_response('version',
                                                      'description',
                                                      'creating')

        description = post['description']
        homepage = post.get('homepage') or ''
        js = post.get('js') or ''
        css = post.get('css') or ''

        if not js and not css:
            return get_no_code_provided_for_version_response(
                version_identifier)

        version = Version(
            version_identifier=version_identifier,
            parent_package=package,
            author=user,
            description=description,
            homepage=homepage,
            js=js,
            css=css,
        )

        try:
            version.full_clean()
            version.save()
        except (Exception, ValidationError) as error:
            if isinstance(error, ValidationError):
                return get_create_error_response('version',
                                                 error=dumps(error.messages),
                                                 status=400)
            else:
                return get_create_error_response('version', version_identifier)

        try:
            # Set the version as the default if it's the only existing version.
            if len(Version.objects.filter(parent_package=package)) == 1:
                package.default_version = version
                package.full_clean()
                package.save()
        except Exception as error:
            print(error)

        return get_item_response(version)
    # Requires version_id pretty url argument
    if method == 'GET' or method == 'DELETE':
        if not version_id:
            return get_id_not_provided_response('version', method)

        if method == 'GET':
            try:
                return get_item_response(Version.objects.get(id=version_id))
            except Version.DoesNotExist:
                return get_item_not_found_response('version',
                                                   version_id)
        # There is no PUT method for versions as they are immutable.
        # TODO: change this so that descriptions and homepages can be changed
        elif method == 'DELETE':
            if not request.user.is_authenticated:
                return get_permission_denied_response('version', method)

            version = Version.objects.get(
                version_identifier=version_identifier)
            if not version:
                return get_item_not_found_response('version',
                                                   version_id)
            elif version.author_id != request.user.id:
                return get_item_not_owned_response('version',
                                                   version_id)
            # Fill in version deletion here.

    return get_method_not_supported_response('version', method)
