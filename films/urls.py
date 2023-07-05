from django.urls import path


from . import views

handler404 = views.handler404

urlpatterns = [
    path('', views.start_page, name='popular'),
    path('viewed', views.viewed_films_list, name='viewed'),
    path('to-watch', views.unseen_list_films, name='to_watch'),
    path('<int:film_id>/', views.film_page, name='film_id')
]
