from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('edit/', views.EditAllView, name='edit all'),
    # path('edit/<int:pk>/', views.EditView, name='edit'),
]
