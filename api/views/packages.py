from json import loads

from django.core.exceptions import ValidationError
from django.db import Error as DatabaseError
from django.forms.models import model_to_dict

from packages.search import packages_search_filter
from packages.models import Package, DeletedPackage
from versions.models import Version

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
        keywords = post.get('keywords') or ''
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

            return get_create_error_response('package', package_id)

        return get_item_response(model_to_dict(package))
    # Requires package_id pretty url argument
    if method == 'GET' or method == 'PUT' or method == 'DELETE':
        if not package_id:
            return get_id_not_provided_response('package', method)

        if method == 'GET':
            to_return = None
            # Retrieve the package.
            if package_id == '*':
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

                package_dicts = []
                # Add the version identifiers to each package.
                for package in models:
                    package_dict = model_to_dict(package)
                    versions = Version.objects.filter(parent_package=package)
                    versions = list(map(lambda x: x.id, versions))
                    package_dict['versions'] = versions
                    package_dict['keywords'] = package.split_keywords()

                    package_dicts.append(package_dict)

                    # Increment the download count for each package.
                    package.downloads += 1
                    try:
                        package.full_clean()
                        package.save()
                    except DatabaseError as error:
                        print(error)

                to_return = package_dicts
            else:
                package = None
                try:
                    package = Package.objects.get(id=package_id)
                except Package.DoesNotExist:
                    return get_item_not_found_response('package',
                                                       package_id)

                package_dict = model_to_dict(package)
                versions = Version.objects.filter(parent_package=package)
                package_dict['versions'] = list(map(
                    lambda x: x.version_identifier, versions))

                # Increment the download count.
                package.downloads += 1
                try:
                    package.full_clean()
                    package.save()
                except DatabaseError as error:
                    print(error)

                to_return = package_dict

            # Send it to the client.
            return get_item_response(to_return)
        elif method == 'PUT':
            user = request.user
            put = loads(request.body)

            if not user.is_authenticated:
                return get_permission_denied_response('package', method)

            package = Package.objects.get(id=package_id)
            if not package:
                return get_item_not_found_response('package', package_id)
            elif package.owner.id != user.id:
                return get_item_not_owned_response('package', package_id)

            if 'description' in put:
                package.description = put['description']

            if 'homepage' in put:
                package.homepage = put['homepage']

            if 'keywords' in put:
                package.keywords = put['keywords']

            if 'default_version' in put:
                default_version = put['default_version']
                version = None
                try:
                    version = Version.objects.get(
                        parent_package=package,
                        version_identifier=default_version)
                except Version.DoesNotExist:
                    return get_version_not_found_error_response(
                        default_version, package.id)

                package.default_version = version

            try:
                package.full_clean()
                package.save()
            except (DatabaseError, ValidationError) as error:
                if isinstance(error, ValidationError):
                    return get_update_error_response(
                        'package', package_id, error=dumps(error.messages),
                        status=400)

                return get_update_error_response('package', package_id)

            item = model_to_dict(package)

            # Send the version identifier, not the version surrogate key.
            default_version = package.default_version
            item['default_version'] = default_version.version_identifier

            return get_item_response(item)
        elif method == 'DELETE':
            user = request.user

            if not user.is_authenticated:
                return get_permission_denied_response('package', method)

            package = Package.objects.get(id=package_id)
            if not package:
                return get_item_not_found_response('package', package_id)
            elif package.owner.id != user.id:
                return get_item_not_owned_response('package', package_id)

            try:
                package.delete()
            except DatabaseError as error:
                print(error)
                return get_update_error_response('package', package.id)

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
