from django.urls import path

from . import views


urlpatterns = [
    path('<int:profile_id>/', views.detail, name='detail'),
]
