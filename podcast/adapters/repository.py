import abc
from typing import List

from podcast.domainmodel.model import Author, Podcast, Category, Episode, User, Playlist, Review

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f"RepositoryException: {message}")


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_podcast(self, podcast: Podcast):
        """ Adds a Podcast to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast(self, podcast_id: int) -> Podcast:
        """ Returns Podcast with id from the repository.
        If there is no Podcast with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts_by_id(self, id_list: list) -> List[Podcast]:
        """ Returns a list of Podcasts, whose ids match those in id_list, from the repository.
        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts_by_page(self, page: int, page_size: int) -> List[Podcast]:
        """ Returns a list of Podcasts for the specified page.
        The list should contain up to page_size podcasts. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_podcasts(self) -> int:
        """ Returns the total number of Podcasts in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts_ids_for_category(self, category_name: str) -> List[int]:
        """ Returns a list of ids representing Podcasts that are in the category: category_name.
        If there are Podcasts that are in the category_name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def has_next_page(self, current_page: int, page_size: int) -> bool:
        """ Returns True if there is a next page, otherwise False. """
        raise NotImplementedError

    @abc.abstractmethod
    def has_previous_page(self, current_page: int) -> bool:
        """ Returns True if there is a previous page, otherwise False. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_page(self, current_page: int, page_size: int) -> int:
        """ Returns the page number of the next page.
        If there is no next page, returns the current page number. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_previous_page(self, current_page: int) -> int:
        """ Returns the page number of the previous page.
        If there is no previous page, returns the current page number. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_categories(self) -> List[Category]:
        """ Returns the Categories stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_episode(self, episode: Episode):
        """ Adds an Episode to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_episodes(self) -> int:
        """ Returns the total number of Episodes in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_episode(self, episode_id: int) -> Episode:
        """ Returns Episode with id from the repository.
        If there is no Podcast with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_author(self, author: Author):
        """ Adds an Author to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_category(self, category: Category):
        """ Adds a Category to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, username: str, password: str):
        """ Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username: str) -> User:
        """ Returns the User named username from the repository.
        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_to_playlist(self, username: str, episode: Episode):
        """ Adds an Episode to the playlist with the given username. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_users_playlist(self, username: str) -> Playlist:
        """ Returns user's playlist with the given username. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, podcast: Podcast, user: User, rating: int, description: str):
        """ Adds a Review to the repository.
        Update User and Podcast's reviews list """
        raise NotImplementedError

    @abc.abstractmethod
    def get_users_reviews(self, username: str) -> List[Review]:
        """ Returns user's reviews list with the given username. '"""
        raise NotImplementedError

    @abc.abstractmethod
    def delete_review(self, review_id: int):
        """ Deletes a Review from the repository.
        Update User and Podcast's reviews list '"""
        raise NotImplementedError
