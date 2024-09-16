from podcast.adapters.repository import AbstractRepository


def get_podcasts_category(repository: AbstractRepository, category):
    return repository.get_podcasts_by_category(category)


def get_podcasts_title(repository: AbstractRepository, title):
    return repository.get_podcasts_by_title(title)


def get_podcasts_author(repository: AbstractRepository, author):
    return repository.get_podcasts_by_author(author)
