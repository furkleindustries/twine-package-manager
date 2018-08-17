from django.urls import path
from . import views


urlpatterns = [
    path('', views.TpmLoginView.as_view(), name='index'),
]
