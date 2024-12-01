from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_title = models.CharField(max_length=200)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie_title} - {self.user.username}"


class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    #release_date = models.DateField()
    poster_url = models.URLField(blank=True, null=True)  # Optional poster image
    rating = models.FloatField(default=0.0)  # Average rating of the movie

    def __str__(self):
        return self.title