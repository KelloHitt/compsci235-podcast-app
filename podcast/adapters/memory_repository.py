import os.path
from typing import List
from pathlib import Path
from podcast.domainmodel.model import Author, Podcast, Episode, Category
from podcast.adapters.repository import AbstractRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__podcasts = list()
        self.__episodes = list()
        self.__authors = dict()
        self.__categories = dict()

    def add_podcast(self, podcast: Podcast):
        self.__podcasts.append(podcast)

    def get_podcast(self, podcast_id: int) -> Podcast:
        return self.__podcasts[podcast_id - 1] if podcast_id < len(self.__podcasts) else None

    def get_podcasts_by_id(self, id_list: list) -> List[Podcast]:
        return [self.get_podcast(podcast_id) for podcast_id in id_list]

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
        self.__episodes.append(episode)

    def get_number_of_episodes(self) -> int:
        return len(self.__episodes)

    def get_episode(self, episode_id: int) -> Episode:
        return self.__episodes[episode_id - 1] if episode_id < len(self.__episodes) else None

    def add_author(self, author: Author):
        self.__authors[author.id] = author

    def add_category(self, category: Category):
        self.__categories[category.id] = category


# Populate the data into memory repository
def populate_data(repo: AbstractRepository):
    data_path = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
    reader = CSVDataReader()
    reader.load_podcasts_authors_categories(data_path)
    reader.load_episodes(data_path)

    podcasts = reader.dataset_of_podcasts
    authors = reader.dataset_of_authors
    categories = reader.dataset_of_categories
    episodes = reader.dataset_of_episodes

    for author in authors:
        repo.add_author(author)

    for podcast in podcasts:
        repo.add_podcast(podcast)

    for category in categories:
        repo.add_category(category)

    for episode in episodes:
        repo.add_episode(episode)
