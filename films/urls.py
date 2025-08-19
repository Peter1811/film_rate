from django.urls import path

from . import views

handler404 = views.handler404

urlpatterns = [
    path('', views.redirect_root),
    path('popular/', views.popular, name='popular'),
    path('my-profile/', views.my_profile_page, name='my_profile'),
    path('add-film/', views.add_film, name='add_film'),
    path('<int:film_id>/', views.film_page, name='film_id'),
    path('watched/', views.film_list, name='watched'),
    path('to-watch/', views.film_list, name='to_watch')
]
