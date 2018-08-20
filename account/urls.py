from django.urls import path

from . import views


urlpatterns = [
    path('', views.AccountView.as_view(), name='index'),
    path('changePassword/', views.change_password, name='change password'),
]
