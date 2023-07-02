from django.db import models


class Film(models.Model):

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self):
        return self.name + ", " + self.genre.lower()

    name = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    annotation = models.TextField(max_length=500)
    rating = models.FloatField(default=0.0)

# Create your models here.
