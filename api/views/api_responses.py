from json import dumps, loads

from django.http import HttpResponse
from django.shortcuts import redirect

from django.forms.models import model_to_dict


def get_method_not_supported_response(_type, method):
    response = HttpResponse(
        dumps({
            'error': 'The request method, ' +
                     '%s, is not supported for requests on type %s.' %
                     (method, _type)
        }),
        status=400,
    )

    response['Content-type'] = 'application/json'
    return response


def get_item_not_found_response(_type, _id):
    response = HttpResponse(
        dumps({
            'error': 'There was no %s found with id %s.' % (_type, _id)
        }),
        status=404,
    )

    response['Content-type'] = 'application/json'
    return response


def get_id_not_provided_response(_type, method):
    response = HttpResponse(
        dumps({
            'error': 'There was no id provided when accessing a ' +
                     '%s with method %s.' % (_type, method)
        }),
        status=400,
    )

    response['Content-type'] = 'application/json'
    return response


def get_id_invalid_response(_type, _id):
    response = HttpResponse(
        dumps({
            'error': 'The id provided, ' +
                     '%s, when accessing a %s was not valid.' % (_type, _id)
        }),
        status=400,
    )

    response['Content-type'] = 'application/json'
    return response


def get_permission_denied_response(_type, method):
    response = HttpResponse(
        dumps({
            'error': 'You must be logged in to access a ' +
                     '%s with method %s.' % (_type, method)
        }),
        status=403,
    )

    response['Content-type'] = 'application/json'
    return response


def get_login_failed_response():
    response = HttpResponse(
        dumps({
            'error': 'The provided login credentials were invalid.'
        }),
        status=403,
    )

    response['Content-type'] = 'application/json'
    return response


def get_item_not_owned_response(_type, _id):
    response = HttpResponse(
        dumps({
            'error': 'The %s with id %s was not owned by the requestor.' %
                     (_type, _id)
        }),
        status=403,
    )

    response['Content-type'] = 'application/json'
    return response


def get_argument_not_provided_response(_type, arg, action):
    response = HttpResponse(
        dumps({
            'error': 'A necessary argument, ' +
                     '%s, was not provided when %s a %s.' %
                     (arg, action, _type)
                     
        }),
        status=400,
    )

    response['Content-type'] = 'application/json'
    return response


def get_argument_invalid_response(_type, arg, value):
    response = HttpResponse(
        dumps({
            'error': 'An invalid value was provided for the argument, %s, ' %
                     (arg) +
                     'when updating a %s. ' % (_type) +
                     'The invalid value was %s.' % (value)
        }),
        status=400,
    )

    response['Content-type'] = 'application/json'
    return response


def get_name_already_exists_response(_type, name):
    response = HttpResponse(
        dumps({
            'error': 'An object of type ' +
                     '%s with name %s already exists. Names must be unique.' %
                     (_type, name)
        }),
        status=400,
    )

    response['Content-type'] = 'application/json'
    return response


def get_update_error(_type, _id, status=500):
    response = HttpResponse(
        dumps({
            'error': 'There was an error in updating a ' +
                     '%s with id %s.' % (_type, _id)
        }),
        status=status or 500,
    )

    response['Content-type'] = 'application/json'
    return response


def get_item_response(item):
    final_form = None
    if isinstance(item, dict):
        final_form = dumps(item)
    else:
        final_form = dumps(model_to_dict(item))

    response = HttpResponse(
        final_form,
        status=200,
    )

    response['Content-type'] = 'application/json'
    return response


def get_redirect_response(url):
    return redirect(url)