from json import loads

from django.core.exceptions import ValidationError
from django.db import Error as DatabaseError
from django.forms.models import model_to_dict

from profiles.models import Profile

from .api_responses import *


def profiles(request, user_id):
    method = request.method

    # Profiles cannot be created through the API.

    # Requires user_id pretty url argument
    if method == 'GET' or method == 'PUT' or method == 'DELETE':
        if not user_id:
            return get_id_not_provided_response('profile', method)

        try:
            user_id = int(user_id)
        except ValueError:
            return get_id_invalid_response('profile', user_id)

        if method == 'GET':
            try:
                profile = Profile.objects.get(user_id=user_id)
                user = profile.user
                profile_dict = {
                    'username': user.username,
                    'user_id': user.id,
                    
                }

                # Respect the user's email visible setting for API requests.
                if profile.email_visible is True:
                    profile_dict.update({
                        'email': user.email,
                    })

                # Modifies the dict in place, so can't be used as a return val.
                profile_dict.update(model_to_dict(profile))

                # The profile ID is used nowhere but as a primary key, so
                # there's really no point in ever exposing it to API consumers.
                del profile_dict['id']

                # Already covered by the user_id key.
                del profile_dict['user']

                # There's no point in showing this field -- either the e-mail
                # is visible to API consumers or it's not.
                del profile_dict['email_visible']

                date_joined = user.date_joined
                profile_dict['date_joined'] = date_joined.isoformat()

                last_login = user.last_login
                profile_dict['last_login'] = last_login.isoformat()

                return get_item_response(profile_dict)
            except Profile.DoesNotExist:
                return get_item_not_found_response('profile', user_id)
        elif method == 'PUT':
            user = request.user
            # Load the data from the JSON body.
            put = loads(request.body)

            if not user.is_authenticated:
                return get_permission_denied_response('profile', method)
            elif user.id != user_id:
                return get_item_not_owned_response('profile', user.id)

            profile = None
            try:
                profile = Profile.objects.get(user_id=user_id)
            except Profile.DoesNotExist:
                pass

            if not profile:
                return get_item_not_found_response('profile', user_id)
            elif profile.user_id != request.user.id:
                return get_item_not_owned_response('profile', user_id)

            if 'description' in put:
                profile.description = put['description'] or ''

            if 'email' in put:
                user.email = put['email']

            if 'email_visible' in put:
                try:
                    profile.email_visible = bool(put['email_visible'])
                except ValueError:
                    profile.email_visible = False

            if 'homepage' in put:
                profile.homepage = put['homepage'] or ''

            if 'date_style' in put:
                date_style = str(put['date_style'])
                if date_style != 'DDMM' and date_style != 'MMDD':
                    return get_argument_invalid_response(
                        'profile',
                        'date_style',
                        date_style)

                profile.date_style = date_style

            if 'time_style' in put:
                time_style = str(put['time_style'])
                if time_style != '12H' and time_style != '24H':
                    return get_argument_invalid_response(
                        'profile',
                        'time_style',
                        time_style)

                profile.time_style = time_style

            try:
                profile.full_clean()
                profile.save()
            except (DatabaseError, ValidationError) as error:
                if isinstance(error, ValidationError):
                    return get_update_error_response(
                        'profile', user.id,
                        error=dumps(error.messages), status=400)
                else:
                    return get_update_error_response(
                        'package', profile.id)

            try:
                user.full_clean()
                user.save()
            except (DatabaseError, ValidationError) as error:
                if isinstance(error, ValidationError):
                    return get_update_error_response(
                        'profile', user.id,
                        error=dumps(error.messages), status=400)
                else:
                    return get_update_error_response(
                        'profile', user.id)

            item = model_to_dict(profile)
            item.update({
                'email': user.email,
            })

            return get_item_response(item)
        elif method == 'DELETE':
            user = request.user
            if not user.is_authenticated:
                return get_permission_denied_response('profile', method)

            profile = Profile.objects.get(id=user_id)
            if not profile:
                return get_item_not_found_response('profile', user_id)
            elif profile.user_id != user.id:
                return get_item_not_owned_response('profile', user_id)

            try:
                profile.delete()
                user.delete()
            except Exception as error:
                print(error)
                return get_update_error_response('profile', user_id)

            return get_item_response({
                'result': 'success',
            })

    return get_method_not_supported_response('profile', method)
