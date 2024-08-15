from typing import List
from podcast.domainmodel.model import Author, Podcast
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Category


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__podcasts = list()
        self.__episodes = list()
        self.__authors = dict()
        self.__categories = dict()

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

    def get_podcast(self, podcast_id: int) -> Podcast:
        return self.__podcasts[podcast_id - 1]

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
