
def context_replenishment_for_film_list_views(slug, context, values):
    if slug == 'viewed':
        context['list_of_films'] = values['viewed']
        context['title'] = 'История просмотров'
    elif slug == 'to-watch':
        context['list_of_films'] = values['to-watch']
        context['title'] = 'Фильмы к просмотру'
