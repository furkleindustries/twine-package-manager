from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from .api_responses import *


@csrf_exempt
def login_view(request):
    method = request.method

    if method != 'POST':
        return get_method_not_supported_response('login', method)

    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username or not password:
        return get_login_failed_response()

    user = authenticate(request, username=username, password=password)
    if not user:
        return get_login_failed_response()

    # We *must* call both authenticate() and login().
    login(request, user)

    return get_item_response({
        'sessionid': request.session._get_or_create_session_key(),
        'csrftoken': get_token(request),
    })
