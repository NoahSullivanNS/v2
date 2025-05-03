from django.shortcuts import render
from django.http import JsonResponse
from .models import Joke
from .tasks import fetch_headlines  # Make sure it returns saved data

def joke_feed(request):
    jokes = Joke.objects.order_by('-fetched_at')[:20]
    return render(request, 'twatter/joke_feed.html', {'jokes': jokes})

def run_fetch_headlines(request):
    if request.method == 'POST':
        fetch_headlines()  # You can make this asynchronous with Celery later
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
