from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template import loader

import films.models
from .models import Film

menu = ['Популярные фильмы', 'История просмотров', 'Фильмы к просмотру', 'Мой профиль']


def handler404(request, exception):
    with open('templates/404.html', 'r') as text_404:
        text = text_404.read()
    response = HttpResponseNotFound(request, content=text)
    response.status_code = 404
    return response

# Create your views here.


def start_page(request):
    return HttpResponse('<h1>Здесь будут показываться популярные фильмы</h1>')


def viewed_films_list(request):
    viewed_films = Film.objects.exclude(rating=0)
    template = loader.get_template('films/films.html')
    context = {
        'list_of_films': viewed_films,
        'title': 'История просмотров',
        'menu': menu
    }
    return HttpResponse(template.render(context, request))


def unseen_list_films(request):
    unseen_films = Film.objects.filter(rating=0)
    template = loader.get_template('films/films.html')
    context = {
        'list_of_films': unseen_films,
        'title': 'Фильмы к просмотру',
        'menu': menu
    }
    return HttpResponse(template.render(context, request))


def film_page(request, film_id):
    try:
        film = Film.objects.get(id=film_id)
        template = loader.get_template('films/film_page.html')
        context = {
            'current_film': film
        }
        return HttpResponse(template.render(context, request))

    except films.models.Film.DoesNotExist:
        raise Http404
