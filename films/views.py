from django.db.models import Q
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
import os

from .forms import FilmForm, genres
from .models import Film
from .utils import context_replenishment_for_film_list_views

menu = {'Популярные фильмы': '',
        'История просмотров': '/viewed',
        'Фильмы к просмотру': '/to-watch',
        'Добавить фильм': '/add-film',
        'Мой профиль': '/my-profile'}

prefix = os.getenv('API_STR')
for item in menu:
    menu[item] = prefix + menu[item]


def handler404(request, exception):
    with open('templates/404.html', 'r') as text_404:
        text = text_404.read()
    response = HttpResponseNotFound(request, content=text)
    response.status_code = 404
    return response


def redirect_root(request):
    return redirect('/films/')


def popular(request):
    context = {
        'title': 'Популярные фильмы',
        'menu': menu
    }
    return render(request, 'films/popular.html', context=context)


def my_profile_page(request):
    context = {
        'title': 'Мой профиль',
        'menu': menu
    }
    return render(request, 'films/my_profile.html', context=context)


@csrf_protect
def film_list(request, film_list_slug):
    context = {
        'menu': menu,
        'genres': genres
    }
    if request.method == 'POST':
        genre = request.POST.get('genre')
        if not genre:
            values = {
                'viewed': Film.objects.filter(~Q(rating=0)),
                'to-watch': Film.objects.filter(rating=0),
            }
            context_replenishment_for_film_list_views(slug=film_list_slug, context=context, values=values)
        else:
            context['requested_genre'] = genre
            values = {
                'viewed': Film.objects.filter(Q(genre=genre) & ~Q(rating=0)),
                'to-watch': Film.objects.filter(Q(genre=genre) & Q(rating=0)),
            }
            context_replenishment_for_film_list_views(slug=film_list_slug, context=context, values=values)
        return render(request, 'films/films_list.html', context=context)

    values = {
        'viewed': Film.objects.filter(~Q(rating=0)),
        'to-watch': Film.objects.filter(rating=0),
    }
    context_replenishment_for_film_list_views(slug=film_list_slug, context=context, values=values)

    return render(request, 'films/films_list.html', context=context)


def film_page(request, film_id):
    try:
        film = Film.objects.get(id=film_id)
        context = {
            'current_film': film,
            'title': film.name,
            'menu': menu
        }
        return render(request, 'films/film_page.html', context=context)

    except Film.DoesNotExist:
        raise Http404


@csrf_protect
def add_film(request):
    if request.method == 'POST' and request.FILES:
        form = FilmForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            film_id = Film.objects.last().id
            return redirect('film_id', film_id)
    else:
        form = FilmForm()

    return render(request, 'films/add_film.html',
                  {'menu': menu, 'title': 'Добавить фильм', 'form': form, 'genres': genres})
