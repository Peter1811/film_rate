from django.urls import path


from . import views

urlpatterns = [
    path('', views.checked_films_list, name='list_of_checked_films'),
    path('<int:film_id>/', views.film_page, name='film_page')
]
