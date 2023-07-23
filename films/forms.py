from django.forms import ModelForm
from .models import Film


class FilmForm(ModelForm):
    class Meta:
        model = Film
        fields = '__all__'

        labels = {
            'name': 'Название фильма',
            'genre': 'Жанр фильма',
            'annotation': 'Краткое описание',
            'rating': 'Рейтинг',
            'poster': 'Постер к фильму'
        }
