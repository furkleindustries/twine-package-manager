from json import loads

from django.utils import timezone
from django.db import Error as DatabaseError
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict

from .api_responses import *

from packages.models import Package, PackageDownload
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

        if 'parentPackageId' not in post:
            return get_version_package_id_not_provided_response()

        package_id = post['parentPackageId']
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
            js=js,
            css=css,
        )

        try:
            version.full_clean()
            version.save()
        except (DatabaseError, ValidationError) as error:
            if isinstance(error, ValidationError):
                return get_create_error_response('version',
                                                 error=dumps(error.messages),
                                                 status=400)
            return get_create_error_response('version', error)

        try:
            # Set the version as the default if it's the only existing version.
            if len(Version.objects.filter(parent_package=package)) == 1:
                package.default_version = version
                package.full_clean()
                package.save()
            else:
                package.date_modified = timezone.now()
        except DatabaseError as error:
            print(error)

        version_dict = model_to_dict(version)
        version_dict['date_created'] = version.date_created.isoformat()

        return get_item_response(version_dict)

    elif method == 'GET':
        version = None
        if version_id:
            try:
                version = Version.objects.get(id=version_id)
            except Version.DoesNotExist:
                return get_item_not_found_response(version_id, 'version')
        else:
            parent_package_id = request.GET.get('parentPackageId')
            version_identifier = request.GET.get('versionIdentifier')
            if not parent_package_id:
                return get_version_package_id_not_provided_response()
            elif not version_identifier:
                return get_version_version_identifier_not_provided_response()

            if version_identifier == 'default':
                version = Package.objects.get(
                    id=parent_package_id
                ).default_version
            else:
                version = Version.objects.get(
                    parent_package__id=parent_package_id,
                    version_identifier=version_identifier,
                )

        if version.parent_package:
            package_download = PackageDownload(package=version.parent_package)
            try:
                package_download.full_clean()
                package_download.save()
            except DatabaseError as err:
                print(err)

        version_dict = model_to_dict(version)
        date_created = version.date_created.isoformat()
        version_dict['date_created'] = date_created
        return get_item_response(version_dict)
    elif method == 'DELETE':
        if not request.user.is_authenticated:
            return get_permission_denied_response('version', method)

        version = Version.objects.get(
            version_identifier=version_identifier)
        if not version:
            return get_item_not_found_response('version', version_id)
        elif version.author_id != request.user.id:
            return get_item_not_owned_response('version', version_id)
        # Fill in version deletion here.

    return get_method_not_supported_response('version', method)

    # There is no PUT method for versions as they are immutable.
