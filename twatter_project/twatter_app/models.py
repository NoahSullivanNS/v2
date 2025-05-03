from django.db import models

class Joke(models.Model):
    headline = models.TextField()
    joke = models.TextField()
    source = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline
