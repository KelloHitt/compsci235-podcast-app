import abc
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    # TODO: implement the abstract methods

    pass
