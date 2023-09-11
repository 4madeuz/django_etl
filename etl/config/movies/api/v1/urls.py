from django.urls import path
from movies.api.v1 import views

urlpatterns = [
    path('movies/', views.MoviesListApi.as_view()),
    path('mov', views.api),
    path('movies/<uuid:id>', views.MoviesDetailApi.as_view()),
]
