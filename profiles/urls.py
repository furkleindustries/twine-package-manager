from django.urls import path

from . import views


urlpatterns = [
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]
