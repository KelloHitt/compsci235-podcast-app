from podcast.adapters.repository import AbstractRepository


def get_podcasts_filtered(repository: AbstractRepository, search_field, search_query):

    if search_field == 'category':
        return repository.get_podcasts_by_category(search_query)
    elif search_field == 'title':
        return repository.get_podcasts_by_title(search_query)
    else:
        return repository.get_podcasts_by_author(search_query)

