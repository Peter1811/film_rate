from django.core.exceptions import ValidationError
from django import forms

from .models import Film

genres = ['Боевик', 'Комедия', 'Ужасы', 'Хоррор', 'Триллер', 'Фэнтези', 'Семейный', 'Приключения']


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['name', 'genre', 'annotation', 'rating', 'poster']
        labels = {
            'name': 'Название фильма',
            'genre': 'Жанр фильма',
            'annotation': 'Краткое описание',
            'rating': 'Рейтинг',
            'poster': 'Постер к фильму',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'annotation': forms.Textarea(attrs={'cols': 50, 'rows': 7}),
        }

    def clean_genre(self):
        genre = self.cleaned_data['genre']
        if genre.lower() not in [_.lower() for _ in genres]:
            raise ValidationError(
                'Такого жанра нет в списке, доступные жанры: ' + ', '.join([_.lower() for _ in genres]))
        return genre

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 0 or rating > 10:
            raise ValidationError('Неверный рейтинг, ожидается значение от 0 (фильм не просмотрен) до 10')
        return rating

