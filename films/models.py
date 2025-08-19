from django.db import models
from django.urls import reverse


class Film(models.Model):

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    name = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    annotation = models.TextField(max_length=500)
    rating = models.FloatField(default=0.0)
    poster = models.ImageField(upload_to='posters/')

    def __str__(self):
        return self.name + ", " + self.genre.lower()

    def get_absolute_url(self):
        return reverse('film_id', kwargs={'film_id': self.pk})

# Create your models here.
