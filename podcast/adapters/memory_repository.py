from typing import List
from podcast.domainmodel.model import Author, Podcast, Episode
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Category


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__podcasts = list()
        self.__episodes = list()
        self.__authors = dict()
        self.__categories = dict()
        # TODO: discuss: maybe we can create a list of podcast with a key value pair where each podcast's value is an episode with their id??

    def add_or_get_author(self, author_name) -> Author:
        if not author_name:
            author_name = "Unknown"
        if author_name not in self.__authors:
            author_id = len(self.__authors) + 1
            author = Author(author_id, author_name)
            self.__authors[author_name] = author
        else:
            author = self.__authors[author_name]
        return author

    def add_podcast(self, podcast: Podcast):
        if podcast not in self.__podcasts:
            self.__podcasts.append(podcast)

    def get_podcast(self, podcast_int: int) -> Podcast:
        return self.__podcasts[podcast_int - 1]

    def get_podcast_by_id(self, podcast_id: int) -> Podcast:
        for podcast1 in self.__podcasts:
            if podcast1.id == podcast_id:
                return podcast1
            return None


    def get_podcasts_by_page(self, page_number: int, page_size: int) -> List[Podcast]:
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        return self.__podcasts[start_index:end_index]

    def get_number_of_podcasts(self) -> int:
        return len(self.__podcasts)

    def get_podcasts_by_id(self, id_list) -> List[Podcast]:
        return [self.get_podcast(podcast_id) for podcast_id in id_list]

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

    def add_or_get_category(self, category_name: str) -> Category:
        if category_name not in self.__categories:
            category_id = len(self.__categories) + 1
            category = Category(category_id, category_name)
            self.__categories[category_name] = category
        else:
            category = self.__categories[category_name]
        return category

    def add_episode(self, episode: Episode):
        if episode not in self.__episodes:
            self.__episodes.append(episode)
            self.__episodes.sort(key=lambda episode: episode.date)

    def get_number_of_episodes(self) -> int:
        return len(self.__episodes)

    # TODO: Review this method, if the episode.id the list index then no need to compare
    def get_episode(self, episode_id: int) -> Episode:
        for episode1 in self.__episodes:
            if episode1._id == episode_id:
                return episode1
