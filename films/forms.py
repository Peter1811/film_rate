from django import forms


class FilmCreate(forms.Form):
    name = forms.CharField(label='Название фильма', max_length=50)
    genre = forms.CharField(label='Жанр фильма', max_length=50)
    annotation = forms.CharField(label='Краткое описание фильма', widget=forms.Textarea, max_length=500)
    rating = forms.FloatField(label='Рейтинг фильма')
