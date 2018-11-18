from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^create/?$', views.CreateView.as_view(), name='create'),
    re_path(r'^search/?$', views.SearchView.as_view(), name='search'),
    re_path(r'^(?P<unique_field>[^/]+)/?$', views.DetailView.as_view(),
            name='detail'),
    re_path(r'^(?P<unique_field>[^/]+)/edit/?$', views.UpdateView.as_view(),
            name='edit'),
    re_path(r'^(?P<unique_field>[^/]+)/delete/?$', views.DeleteView.as_view(),
            name='delete'),
    re_path(r'^(?P<unique_field>[^/]+)/create_version/?$',
            views.CreateVersionView.as_view(), name='create version')
]
