from django.urls import path, re_path

from .views import login_view, packages, profiles, versions


urlpatterns = [
    path('login/', login_view, name='login API'),
    re_path(r'^packages/(.+|\*)?/?$', packages, name='packages API'),
    re_path(r'^profiles/(\d+|\*)?/?$', profiles, name='profiles API'),
    re_path(r'^versions/(\d+)?/?$', versions, name='versions API'),
]
