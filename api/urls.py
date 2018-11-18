from django.urls import path, re_path

from .views import (
    PackageList, PackageDetail, PackageTopDownloads,
    PackagesMostRecentlyModified, ProfileList, ProfileDetail, VersionList,
    VersionDetail,
)

urlpatterns = [
    re_path(r'^packages/?$', PackageList.as_view(), name='Packages list'),
    re_path(r'^packages_top_downloads/?', PackageTopDownloads.as_view(),
            name='Packages top downloads'),
    re_path(r'^packages_recently_modified/?',
            PackagesMostRecentlyModified.as_view(),
            name='Packages recently modified'),
    re_path(r'^packages/(?P<field>[^/]+)?/?$', PackageDetail.as_view(),
            name='Packages detail'),

    re_path(r'^profiles/?$', ProfileList.as_view(), name='Profiles list'),
    re_path(r'^profiles/(?P<user_id>\d+)?/?$', ProfileDetail.as_view(),
            name='Profiles detail'),

    re_path(r'^versions/?$', VersionList.as_view(), name='Versions list'),
    re_path(r'^versions/(?P<field>[^/]+)?/?$', VersionDetail.as_view(),
            name='Versions detail'),
]
