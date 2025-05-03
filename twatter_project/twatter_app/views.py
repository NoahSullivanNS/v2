from django.shortcuts import render
from .tasks import fetch_headlines

def joke_feed(request):
    headlines = fetch_headlines()
    return render(request, 'twatter/joke_feed.html', {'headlines': headlines})

from django.shortcuts import render
from .models import Joke

def homepage(request):
    jokes = Joke.objects.order_by('-fetched_at')[:20]
    return render(request, 'twatter/home.html', {'jokes': jokes})
