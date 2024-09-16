from podcast.adapters.repository import AbstractRepository


def get_podcasts_get_podcasts_filtered(repository: AbstractRepository, search_query):
    if search_query == 'category':
        repository.get_podcasts_by_category(search_query)
    elif search_query == 'title':
        return repository.get_podcasts_by_title(search_query)
    else:
        return repository.get_podcasts_by_author(search_query)

