from json import loads
from re import split

from django.core.exceptions import ValidationError
from django.db import Error as DatabaseError
from django.forms.models import model_to_dict

from packages.search import packages_search_filter
from packages.models import (
    Package, DeletedPackage, PackageDownload, split_keywords)

from versions.models import Version

from .api_responses import *


def get_full_package_dict(package, include_versions=False):
    package_dict = model_to_dict(package)
    versions = Version.objects.filter(parent_package=package)
    if not include_versions:
        versions = list(map(lambda x: x.version_identifier, versions))

    default_version = package.default_version
    if default_version:
        default_version = default_version.version_identifier

    downloads = PackageDownload.objects.filter(package=package).count()

    package_dict.update({
        'date_created': package.date_created.isoformat(),
        'date_modified': package.date_modified.isoformat(),
        'default_version': default_version,
        'downloads': downloads,
        'versions': versions,
    })

    return package_dict


def version_is_default(version, package):
    has_default = bool(package.default_version)
    is_default = None
    if has_default:
        is_default = version == package.default_version

    return has_default and is_default


def version_identifier_included(version, include_versions):
    return version.version_identifier in include_versions


def version_id_to_version(version_id):
    return Version.objects.get(id=version_id)


def packages(request, package_name):
    method = request.method

    if method == 'POST':
        user = request.user
        post = loads(request.body)

        if not user.is_authenticated:
            return get_permission_denied_response('package', method)

        name = post.get('name')
        description = post.get('description')

        homepage = post.get('homepage') or ''
        if homepage and not homepage.startswith('http'):
            homepage = 'http://' + homepage

        keywords = post.get('keywords') or '[]'
        tag = post.get('tag') or ''

        if not name:
            return get_argument_not_provided_response('package', 'name',
                                                      'creating')

        keywords = split_keywords(keywords)

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

        already_deleted_package = None
        try:
            already_deleted_package = DeletedPackage.objects.get(name=name)
        except DeletedPackage.DoesNotExist:
            pass

        if already_deleted_package:
            return get_package_already_deleted_response(name)

        package = Package(
            author=user,
            description=description,
            homepage=homepage,
            keywords=keywords,
            name=name,
            owner=user,
            tag=tag,
        )

        try:
            package.full_clean()
            package.save()
        except (DatabaseError, ValidationError) as error:
            if isinstance(error, ValidationError):
                return get_create_error_response('package',
                                                 error=dumps(error.messages),
                                                 status=400)

            return get_create_error_response('package', package_name)

        return get_item_response(get_full_package_dict(package))
    # Requires package_name pretty url argument
    if method == 'GET' or method == 'PUT' or method == 'DELETE':
        if not package_name:
            return get_id_not_provided_response('package', method)

        if method == 'GET':
            to_return = None
            # Retrieve the package.
            if package_name == '*':
                cursor = request.GET.get('cursor') or None
                if cursor:
                    cursor = int(cursor)

                quantity = request.GET.get('quantity') or None
                if quantity:
                    quantity = int(quantity)

                models = Package.objects.all()

                search = request.GET.get('search') or None
                if search:
                    models = packages_search_filter(search, models)

                if cursor is not None:
                    models = models.filter(id__gte=cursor)

                # Slice the result if a quantity was provided.
                if quantity is not None:
                    models = models[0:quantity]

                to_return = list(map(get_full_package_dict, models))
            else:
                package = None
                try:
                    package = Package.objects.get(name=package_name)
                except Package.DoesNotExist:
                    return get_item_not_found_response('package', package_name)

                to_return = None

                include_versions = request.GET.get('includeVersions') or None
                if include_versions:
                    to_return = get_full_package_dict(package,
                                                      include_versions=True)

                    include_versions = split(r',? *', include_versions)
                    versions = to_return['versions']

                    version_map = {}
                    for version in versions:
                        is_included = version_identifier_included(
                            version, include_versions)

                        has_def = 'default' in include_versions
                        is_default_included = (has_def and
                                               version_is_default(
                                                   version, package))

                        # Skip versions not included.
                        if not is_included and not is_default_included:
                            continue

                        vers_dict = model_to_dict(version)
                        date_created = version.date_created.isoformat()
                        vers_dict['date_created'] = date_created

                        include_default = 'default' in include_versions
                        is_default = version.id == package.default_version.id
                        if include_default and is_default:
                            version_map['default'] = vers_dict
                        else:
                            version_map[version.version_identifier] = vers_dict

                        p_dl = PackageDownload.objects.create(package=package)
                        try:
                            p_dl.full_clean()
                            p_dl.save()
                        except DatabaseError as err:
                            print(err)

                        # Ensure the returned value reflects the requested
                        # downloads.
                        to_return['downloads'] += 1

                    to_return['versions'] = version_map
                else:
                    to_return = get_full_package_dict(package)

            # Send it to the client.
            return get_item_response(to_return)
        elif method == 'PUT':
            user = request.user
            put = loads(request.body)

            if not user.is_authenticated:
                return get_permission_denied_response('package', method)

            package = Package.objects.get(name=package_name)
            if not package:
                return get_item_not_found_response('package', package_name)
            elif package.owner.id != user.id:
                return get_item_not_owned_response('package', package_name)

            if 'description' in put:
                package.description = put['description']

            if 'homepage' in put:
                package.homepage = put['homepage']

            if 'keywords' in put:
                package.keywords = split_keywords(put['keywords'])

            if 'default_version' in put:
                default_version = put['default_version']
                version = None
                try:
                    version = Version.objects.get(
                        parent_package=package,
                        version_identifier=default_version)
                except Version.DoesNotExist:
                    return get_version_not_found_error_response(
                        default_version, package_name)

                package.default_version = version

            try:
                package.full_clean()
                package.save()
            except (DatabaseError, ValidationError) as error:
                if isinstance(error, ValidationError):
                    return get_update_error_response(
                        'package', package_name, error=dumps(error.messages),
                        status=400)

                return get_update_error_response('package', package_name)

            return get_item_response(get_full_package_dict(package))
        elif method == 'DELETE':
            user = request.user

            if not user.is_authenticated:
                return get_permission_denied_response('package', method)

            package = Package.objects.get(name=package_name)
            if not package:
                return get_item_not_found_response('package', package_name)
            elif package.owner.id != user.id:
                return get_item_not_owned_response('package', package_name)

            try:
                package.delete()
            except DatabaseError as error:
                print(error)
                return get_update_error_response('package', package_name)

            deleted_package = DeletedPackage(
                name=package.name,
                owner_id=package.owner.id,
            )

            try:
                deleted_package.full_clean()
                deleted_package.save()
            except DatabaseError as err:
                print(err)

            return get_item_response({
                'result': 'success',
            })

    return get_method_not_supported_response('package', method)
