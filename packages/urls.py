from django.urls import path

from . import views

urlpatterns = [
    path('<int:package_id>/', views.detail, name='packages'),
]
