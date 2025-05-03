from django.urls import path
from . import views

urlpatterns = [
    path('', views.joke_feed, name='joke_feed'),
    path('home/', views.homepage, name='homepage'),
]
