from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template import loader
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView
from django.core.files.storage import FileSystemStorage
import os

from .models import Film
from .forms import FilmForm

menu = {'Популярные фильмы': '',
        'История просмотров': '/viewed',
        'Фильмы к просмотру': '/to-watch',
        'Добавить фильм': '/add-film',
        'Мой профиль': '/my-profile'}

prefix = os.getenv('API_STR')
for item in menu:
    menu[item] = prefix + menu[item]


class FilmCreate(CreateView):
    model = Film
    form_class = FilmForm
    extra_context = {}
    template_name = 'films/add_film.html'
    success_url = '/films'


def handler404(request, exception):
    with open('templates/404.html', 'r') as text_404:
        text = text_404.read()
    response = HttpResponseNotFound(request, content=text)
    response.status_code = 404
    return response


def redirect_root(request):
    return redirect('/films/')


def popular(request):
    template = loader.get_template('films/popular.html')
    context = {
        'title': 'Популярные фильмы',
        'menu': menu
    }
    return HttpResponse(template.render(context, request))


def my_profile_page(request):
    template = loader.get_template('films/my_profile.html')
    context = {
        'title': 'Мой профиль',
        'menu': menu
    }
    return HttpResponse(template.render(context, request))


def viewed_films_list(request):
    viewed_films = Film.objects.exclude(rating=0)
    template = loader.get_template('films/films_list.html')
    context = {
        'list_of_films': viewed_films,
        'title': 'История просмотров',
        'menu': menu
    }
    return HttpResponse(template.render(context, request))


def unseen_list_films(request):
    unseen_films = Film.objects.filter(rating=0)
    template = loader.get_template('films/films_list.html')
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
            'current_film': film,
            'title': film.name,
            'menu': menu
        }
        return HttpResponse(template.render(context, request))

    except Film.DoesNotExist:
        raise Http404


@csrf_protect
def add_film(request):
    template = loader.get_template('films/add_film.html')
    context = {
        'title': 'Добавление фильма',
        'menu': menu
    }
    if request.method == 'POST' and request.FILES:
        file = request.FILES['film_poster']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        film_url = fs.url(filename)
        context['film_url'] = film_url
        return HttpResponse(template.render(context, request))

    return HttpResponse(template.render(context, request))
