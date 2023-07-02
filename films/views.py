from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Film

# Create your views here.


def checked_films_list(request):
    checked_films = Film.objects.exclude(rating=0)
    template = loader.get_template('films/films.html')
    context = {
        'list_of_checked_films': checked_films
    }
    return HttpResponse(template.render(context, request))


def film_page(request, film_id):
    film = Film.objects.get(id=film_id)
    template = loader.get_template('films/film_page.html')
    context = {
        'current_film': film
    }
    return HttpResponse(template.render(context, request))


