from django.urls import path
from . import views

urlpatterns = [
    path('', views.joke_feed, name='joke_feed'),
    path('run-fetch/', views.run_fetch_headlines, name='run_fetch_headlines'),
]
