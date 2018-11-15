from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('<str:name>/', views.DetailView.as_view(), name='detail'),
    path('<str:name>/edit/', views.UpdateView.as_view(), name='edit'),
    path('<str:name>/delete/', views.DeleteView.as_view(), name='delete'),
    path('<str:name>/create_version/', views.CreateVersionView.as_view(),
         name='create version')
]
