from django.urls import path

from . import views

handler404 = views.handler404

urlpatterns = [
    path('', views.popular, name='popular'),
    path('my-profile/', views.my_profile_page, name='my_profile'),
    path('add-film/', views.add_film, name='add_film'),
    path('<int:film_id>/', views.film_page, name='film_id'),
    path('<slug:film_list_slug>/', views.film_list, name='film_list'),
]
