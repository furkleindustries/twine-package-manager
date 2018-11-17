from django.urls import path, re_path

from .views import (
    PackageList, PackageDetail, ProfileList, ProfileDetail, VersionList,
    VersionDetail,
)

urlpatterns = [
    re_path(r'^packages/?$', PackageList.as_view(), name='Packages list'),
    re_path(r'^packages/(?P<field>\S+)?/?$', PackageDetail.as_view(),
            name='Packages detail'),

    re_path(r'^profiles/?$', ProfileList.as_view(), name='Profiles list'),
    re_path(r'^profiles/(?P<pk>\d+)?/?$', ProfileDetail.as_view(),
            name='Profiles detail'),

    re_path(r'^versions/?$', VersionList.as_view(), name='Versions list'),
    re_path(r'^versions/(?P<pk>\d+)?/?$', VersionDetail.as_view(),
            name='Versions detail'),
]
