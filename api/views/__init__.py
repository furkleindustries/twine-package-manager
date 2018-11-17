# Note: every request that needs authentication *should* be
# authenticated if it makes it past the Django CSRF middleware. Ergo,
# there is *probably* no need to check for authentication inside the API views.
# We're doing it anyway out of an abundance of caution.
#
# To authenticate remotely (e.g. through cURL or XHR), three pieces are needed.
# 1.) A csrftoken cookie.
# 2.) A sessionid cookie.
# 3.) The X-CSRFToken header, with the same value as the csrftoken cookie.
#
# Both of the values needed for this can be obtained one of two ways:
# 1.) POST the credentials to the /api/login/ route and parse the response.
# 2.) GET the /login/ route, scrape the csrftoken cookie, and POST that and
#     username/password arguments to the /login/ route.

from .login import *
from .packages import *
from .profiles import *
from .versions import *
from .drf_views import *
