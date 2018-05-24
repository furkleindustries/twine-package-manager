from django.urls import path

from . import views


urlpatterns = [
    path('packages/<int:package_id>/', views.packages, name='packages API'),
    path('profiles/<int:profile_id>/', views.profiles, name='profiles API'),
    path('versions/<int:version_id>/', views.versions, name='versions API'),
]
