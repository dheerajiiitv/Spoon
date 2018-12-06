from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'MoviesHub'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('movie_details/<int:movie_id>', views.get_movie_details, name='movie_details'),
]
