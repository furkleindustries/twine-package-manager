from django.urls import path

from . import views


urlpatterns = [
    path('', views.TpmLogoutView.as_view(), name='index')
]
