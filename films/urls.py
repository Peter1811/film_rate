from django.urls import path


from . import views

handler404 = views.handler404

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('popular/', views.popular, name='popular'),
    path('my-profile/', views.my_profile_page, name='my_profile'),
    path('viewed/', views.viewed_films_list, name='viewed'),
    path('to-watch/', views.unseen_list_films, name='to_watch'),
    path('<int:film_id>/', views.film_page, name='film_id'),
    path('add-film/', views.add_film, name='add_film')
]
