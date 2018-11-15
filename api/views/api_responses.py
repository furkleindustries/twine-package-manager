from datetime import datetime
from json import dumps

from django.http import HttpResponse
from django.shortcuts import redirect


def with_default_headers(response):
    response['Content-type'] = 'application/json'
    return response


def get_method_not_supported_response(_type, method):
    response = HttpResponse(
        dumps({
            'error': 'The request method, {}, is not '.format(method) +
                     'supported for requests on type {}.'.format(_type)
        }),
        status=400,
    )

    return with_default_headers(response)


def get_item_not_found_response(_type, _id):
    response = HttpResponse(
        dumps({
            'error': 'There was no {} found with id {}.'.format(_type, _id)
        }),
        status=404,
    )

    return with_default_headers(response)


def get_id_not_provided_response(_type, method):
    response = HttpResponse(
        dumps({
            'error': 'There was no id provided when accessing a ' +
                     '{} with method {}'.format(_type, method)
        }),
        status=400,
    )

    return with_default_headers(response)


def get_id_invalid_response(_type, _id):
    response = HttpResponse(
        dumps({
            'error': 'The id provided when accessing a {}, '.format(_type) +
                     '{}, was not valid.'.format(_id)
        }),
        status=400,
    )

    return with_default_headers(response)


def get_version_package_id_not_provided_response():
    response = HttpResponse(
        dumps({
            'error': 'There was no packageId provided when trying to ' +
                     'create, read, or delete a version.'
        }),
        status=400,
    )

    return with_default_headers(response)


def get_version_version_identifier_not_provided_response():
    response = HttpResponse(
        dumps({
            'error': 'There was no versionIdentifier provided when trying ' +
                     'to create, read, or delete a version.'
        }),
        status=400,
    )

    return with_default_headers(response)


def get_version_already_exists_response(package_id, version_id):
    response = HttpResponse(
        dumps({
            'error': 'The package with id {} already possesses a version '
                     .format(package_id) +
                     'with the identifier {}.'.format(version_id),
        }),
        status=400,
    )

    return with_default_headers(response)


def get_no_code_provided_for_version_response(version_id):
    response = HttpResponse(
        dumps({
            'error': 'No code was submitting (neither JS nor CSS) for a ' +
                     'version with identifier {}.'.format(version_id)
        }),
        status=400,
    )

    return with_default_headers(response)


def get_permission_denied_response(_type, method):
    response = HttpResponse(
        dumps({
            'error': 'You must be logged in to access a ' +
                     '{} with method {}.'.format(_type, method)
        }),
        status=403,
    )

    return with_default_headers(response)


def get_login_failed_response():
    response = HttpResponse(
        dumps({
            'error': 'The provided login credentials were invalid.'
        }),
        status=403,
    )

    return with_default_headers(response)


def get_item_not_owned_response(_type, _id):
    response = HttpResponse(
        dumps({
            'error': 'The {} with id {} was not owned by the requestor.'
                     .format(_type, _id)
        }),
        status=403,
    )

    return with_default_headers(response)


def get_argument_not_provided_response(_type, arg, action):
    response = HttpResponse(
        dumps({
            'error': 'A necessary argument, ' +
                     '{}, was not provided when {} a {}.'
                     .format(arg, action, _type)
        }),
        status=400,
    )

    return with_default_headers(response)


def get_argument_invalid_response(_type, arg, value):
    response = HttpResponse(
        dumps({
            'error': 'An invalid value was provided for ' +
                     'the argument, {}, '.format(arg) +
                     'when updating a {}. '.format(_type) +
                     'The invalid value was {}.'.format(value)
        }),
        status=400,
    )

    return with_default_headers(response)


def get_name_already_exists_response(_type, name):
    response = HttpResponse(
        dumps({
            'error': 'An object of type ' +
                     '{} with name {} already exists. Names must be unique.'
                     .format(_type, name)
        }),
        status=400,
    )

    return with_default_headers(response)


def get_package_already_deleted_response(name):
    response = HttpResponse(
        dumps({
            'error': 'A package with the name {} '.format(name) +
                     'was already created, then deleted. For security ' +
                     'reasons, TwinePM does not allow creating packages ' +
                     'with names that have previously existed.',
        }),
        status=400,
    )

    return with_default_headers(response)


def get_create_error_response(_type, error=None, status=500):
    response = HttpResponse(
        dumps({
            'error': error or ('There was an error in creating a {}.'
                               .format(_type))
        }),
        status=status or 500,
    )

    return with_default_headers(response)


def get_update_error_response(_type, _id, status=500, error=None):
    response = HttpResponse(
        dumps({
            'error': error or ('There was an error in updating a ' +
                               '{} with id {}.'.format(_type, _id))
        }),
        status=status or 500,
    )

    return with_default_headers(response)


def get_version_not_found_error_response(package_id, version_identifier):
    response = HttpResponse(
        dumps({
            'error': 'There was no version with the version identifier ' +
                     '{} found for the package with id {}.'
                     .format(package_id, version_identifier)
        }),
        status=400,
    )

    return with_default_headers(response)


def get_item_response(item):
    json = dumps(item)
    response = HttpResponse(json)
    return with_default_headers(response)


def get_redirect_response(url):
    return redirect(url)
