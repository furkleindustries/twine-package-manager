from django.urls import path, re_path

from .views import login_view, packages, profiles, versions
from .views.drf_views import (
    PackageList, PackageDetail, ProfileList, ProfileDetail, VersionList,
    VersionDetail,
)

urlpatterns = [
    path('login/', login_view, name='login API'),
    re_path(r'^packages/(.+|\*)?/?$', packages, name='packages API'),
    re_path(r'^profiles/(\d+|\*)?/?$', profiles, name='profiles API'),
    re_path(r'^versions/(\d+)?/?$', versions, name='versions API'),

    re_path(r'^drf-packages/?$', PackageList.as_view(), name='drf packages'),
    re_path(r'^drf-packages/(?P<field>\S+)?/?$', PackageDetail.as_view(),
            name='drf packages'),

    re_path(r'^drf-profiles/?$', ProfileList.as_view(), name='drf profiles'),
    re_path(r'^drf-profiles/(?P<pk>\d+)?/?$', ProfileDetail.as_view(),
            name='drf profiles'),

    re_path(r'^drf-versions/?$', VersionList.as_view(), name='drf versions'),
    re_path(r'^drf-versions/(?P<pk>\d+)?/?$', VersionDetail.as_view(),
            name='drf versions'),
]
