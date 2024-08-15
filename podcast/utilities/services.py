from podcast.adapters.repository import AbstractRepository


def get_categories(repository: AbstractRepository):
    categories = repository.get_categories()
    return categories
