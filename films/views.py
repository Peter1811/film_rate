from django.db.models import Q
from django.http import HttpResponseNotFound, Http404, HttpRequest
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
import os

from .forms import FilmForm, genres
from .models import Film

menu = {
    # 'Популярные фильмы': '/popular',
    'История просмотров': '/watched',
    'Фильмы к просмотру': '/to-watch',
    'Добавить фильм': '/add-film',
    # 'Мой профиль': '/my-profile'
}


def handler404(request: HttpRequest, exception):
    with open('templates/404.html', 'r') as text_404:
        text = text_404.read()
    response = HttpResponseNotFound(request, content=text)
    response.status_code = 404
    return response


def redirect_root(request: HttpRequest):
    return redirect('/popular/')


def popular(request: HttpRequest):
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
def film_list(request: HttpRequest):
    '''
    Получение списка фильмов - либо просмотренных, либо запланированных
    к просмотру (в зависимости от path).

    :param request: передаваемый запрос.
    '''

    context = {
        'menu': menu,
        'genres': genres
    }
    path = request.path
    
    if request.method == 'POST':
        genre = request.POST.get('genre')
        if not genre or genre == 'все жанры':
            if path == '/watched/':
                context['list_of_films'] = Film.objects.filter(
                    ~Q(rating=0)
                )
                context['title'] = 'Просмотрено'
            elif path == '/to-watch/':
                context['list_of_films'] = Film.objects.filter(
                    Q(rating=0)
                )
                context['title'] = 'Запланировано к просмотру'

        else:
            context['requested_genre'] = genre
            if path == '/watched/':
                context['list_of_films'] = Film.objects.filter(
                    Q(genre=genre) & ~Q(rating=0)
                )
                context['title'] = 'Просмотрено'
            elif path == '/to-watch/':
                context['list_of_films'] = Film.objects.filter(
                    Q(genre=genre) & Q(rating=0)
                )
                context['title'] = 'Запланировано к просмотру'

        context['list_type'] = '_'.join(path.strip('/').split('-'))
        return render(request, 'films/films_list.html', context=context)

    if path == '/watched/':
        context['list_of_films'] = Film.objects.filter(~Q(rating=0))
        context['title'] = 'Просмотрено'
    elif path == '/to-watch/':
        context['list_of_films'] = Film.objects.filter(Q(rating=0))
        context['title'] = 'Запланировано к просмотру'

    context['list_type'] = '_'.join(path.strip('/').split('-'))
    return render(
        request, 
        'films/films_list.html', 
        context=context
    )


def film_page(request: HttpRequest, film_id: int):
    '''
    Страница с данными о фильме.

    :param request: передаваемый запрос;
    :param film_id: id фильма.
    '''

    try:
        back_list = request.GET.get('from')
        film = Film.objects.get(id=film_id)
        context = {
            'current_film': film,
            'title': film.name,
            'menu': menu,
            'back_list': back_list
        }
        return render(
            request, 
            'films/film_page.html', 
            context=context
        )

    except Film.DoesNotExist:
        raise Http404


@csrf_protect
def add_film(request: HttpRequest):
    '''
    Добавление фильма по полям из формы FilmForm.

    :param request: передаваемый запрос.
    '''

    context = {
        'menu': menu, 
        'title': 'Добавить фильм',
        'genres': genres,
        'back_list': None
    }

    if request.method == 'POST' and request.FILES:
        form = FilmForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            film_id = Film.objects.last().id
            return redirect('film_id', film_id)
    else:
        form = FilmForm()

    context['form'] = form
    return render(
        request, 
        'films/add_film.html',
        context=context   
    )
