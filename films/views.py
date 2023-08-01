from django.db.models import Q
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
import os

from .models import Film
from .forms import FilmForm, genres

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
def viewed_films_list(request):
    context = {
        'title': 'История просмотров',
        'menu': menu,
        'genres': genres
    }
    if request.method == 'POST':
        genre = request.POST.get('genre')
        context['list_of_films'] = Film.objects.filter(Q(genre=genre) & ~Q(rating=0))
        context['requested_genre'] = genre
        return render(request, 'films/films_list.html', context=context)

    context['list_of_films'] = Film.objects.filter(~Q(rating=0))

    return render(request, 'films/films_list.html', context=context)


@csrf_protect
def unseen_list_films(request):
    context = {
        'title': 'Фильмы к просмотру',
        'menu': menu,
        'genres': genres
    }
    if request.method == 'POST':
        genre = request.POST.get('genre')
        context['list_of_films'] = Film.objects.filter(Q(genre=genre) & Q(rating=0))
        context['requested_genre'] = genre
        return render(request, 'films/films_list.html', context=context)

    context['list_of_films'] = Film.objects.filter(rating=0)

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
