import bisect
from pathlib import Path
from typing import List

from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Author, Podcast, Episode, Category, User


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__podcasts = list()
        self.__episodes = list()
        self.__authors = dict()
        self.__categories = dict()
        self.__podcasts_by_id = dict()
        self.__users = list()

    def add_podcast(self, podcast: Podcast):
        if podcast not in self.__podcasts:
            self.__podcasts_by_id[podcast.id] = podcast
            bisect.insort(self.__podcasts, podcast, key=lambda p: p.title.lower())

    def get_podcast(self, podcast_id: int) -> Podcast:
        return self.__podcasts_by_id.get(podcast_id) if podcast_id <= len(self.__podcasts) else None

    def get_podcasts_by_id(self, id_list: list) -> List[Podcast]:
        podcasts = [self.get_podcast(podcast_id) for podcast_id in id_list]
        return sorted(podcasts, key=lambda p: p.title.lower())

    def get_podcasts_by_page(self, page_number: int, page_size: int) -> List[Podcast]:
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        return self.__podcasts[start_index:end_index]

    def get_number_of_podcasts(self) -> int:
        return len(self.__podcasts)

    def get_podcasts_ids_for_category(self, category_name: str) -> List[int]:
        matching_podcast_ids = []
        for podcast in self.__podcasts:
            if any(category.name == category_name for category in podcast.categories):
                matching_podcast_ids.append(podcast.id)
        return matching_podcast_ids

    def has_next_page(self, current_page: int, page_size: int) -> bool:
        total_podcasts = self.get_number_of_podcasts()
        return current_page * page_size < total_podcasts

    def has_previous_page(self, current_page: int) -> bool:
        return current_page > 1

    def get_next_page(self, current_page: int, page_size: int) -> int:
        if self.has_next_page(current_page, page_size):
            return current_page + 1
        return current_page

    def get_previous_page(self, current_page: int) -> int:
        if self.has_previous_page(current_page):
            return current_page - 1
        return current_page

    def get_categories(self) -> List[Category]:
        categories = list(self.__categories.values())
        sorted_categories = sorted(categories, key=lambda category: category.name)  # Sort the categories by names
        return sorted_categories

    def add_episode(self, episode: Episode):
        if episode not in self.__episodes:
            self.__episodes.append(episode)

    def get_number_of_episodes(self) -> int:
        return len(self.__episodes)

    def get_episode(self, episode_id: int) -> Episode:
        return self.__episodes[episode_id - 1] if episode_id <= len(self.__episodes) else None

    def add_author(self, author: Author):
        self.__authors[author.name] = author

    def add_category(self, category: Category):
        self.__categories[category.name] = category

    def add_user(self, username: str, password: str):
        new_user = User((len(self.__users) + 1), username, password)
        self.__users.append(new_user)

    def get_user(self, username) -> User:
        return next((user for user in self.__users if user.username == username), None)

    def add_to_playlist(self, username: str, episode: Episode):
        user = self.get_user(username)
        if not user:
            raise ValueError(f'User {username} is not found!')
        if user.playlist is None:
            user.create_playlist(f'{username}s Playlist')
        user.playlist.add_episode(episode)


# Populate the data into memory repository
def populate_data(repo: AbstractRepository, data_path: Path):
    reader = CSVDataReader()
    reader.load_podcasts_authors_categories(data_path)
    reader.load_episodes(data_path)

    podcasts = reader.dataset_of_podcasts
    authors = reader.dataset_of_authors
    categories = reader.dataset_of_categories
    episodes = reader.dataset_of_episodes

    for author in authors.values():
        repo.add_author(author)

    for podcast in podcasts:
        repo.add_podcast(podcast)

    for category in categories.values():
        repo.add_category(category)

    for episode in episodes:
        repo.add_episode(episode)
