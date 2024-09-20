import csv
from pathlib import Path

from podcast.domainmodel.model import Podcast, Episode, Category, Author, Review, User


class CSVDataReader:
    def __init__(self):
        self.__dataset_of_podcasts = list()
        self.__dataset_of_episodes = list()
        self.__dataset_of_authors = dict()
        self.__dataset_of_categories = dict()
        self.__dataset_of_reviews = list()

    def read_csv_file(self, filename: str):
        with open(filename, 'r', newline='', encoding='utf-8-sig') as csv_file:
            reader = csv.reader(csv_file)

            # Read column names of the CSV file
            column_names = next(reader)

            # Read remaining rows from the CSV file
            for row in reader:
                row = [item.strip() for item in row]
                yield row

    def load_podcasts_authors_categories(self, data_path: Path):
        podcasts_filename = str(data_path / "podcasts.csv")
        for data_row in self.read_csv_file(podcasts_filename):
            podcast_id = int(data_row[0])
            podcast_title = data_row[1]
            image = data_row[2]
            description = data_row[3]
            language = data_row[4]
            categories = [category.strip() for category in data_row[5].split('|')]
            website = data_row[6]
            podcast_author = self.add_or_get_author(data_row[7])
            itunes_id = int(data_row[8])
            new_podcast = Podcast(podcast_id, podcast_author, podcast_title, image, description, website,
                                  itunes_id, language)

            # add podcast to author's podcast list
            podcast_author.add_podcast(new_podcast)

            # add podcast to categories
            for category in categories:
                podcast_category = self.add_or_get_category(category)
                new_podcast.add_category(podcast_category)

            # add podcast to the list for future access
            self.__dataset_of_podcasts.append(new_podcast)

    def load_episodes(self, data_path: Path):
        episodes_filename = str(data_path / "episodes.csv")
        for data_row in self.read_csv_file(episodes_filename):
            episode_id = int(data_row[0])
            podcast_id = int(data_row[1])
            title = data_row[2]
            audio = data_row[3]
            audio_length = int(data_row[4])
            description = data_row[5]
            pub_date = data_row[6]
            pub_date_sliced = pub_date[0:-3]
            podcast = self.get_podcast_by_id(podcast_id)
            new_episode = Episode(episode_id, podcast, title, audio, description, audio_length, pub_date_sliced)
            if podcast is not None:
                podcast.add_episode(new_episode)
            self.__dataset_of_episodes.append(new_episode)


    def add_or_get_author(self, author_name) -> Author:
        if not author_name:
            author_name = "Unknown"
        if author_name not in self.__dataset_of_authors:
            author_id = len(self.__dataset_of_authors) + 1
            author = Author(author_id, author_name)
            self.__dataset_of_authors[author_name] = author
        else:
            author = self.__dataset_of_authors[author_name]
        return author

    def add_or_get_category(self, category_name: str) -> Category:
        if category_name not in self.__dataset_of_categories:
            category_id = len(self.__dataset_of_categories) + 1
            category = Category(category_id, category_name)
            self.__dataset_of_categories[category_name] = category
        else:
            category = self.__dataset_of_categories[category_name]
        return category

    def get_podcast_by_id(self, podcast_id: int) -> Podcast:
        return self.__dataset_of_podcasts[podcast_id - 1] if podcast_id < len(self.__dataset_of_podcasts) else None

    @property
    def dataset_of_podcasts(self):
        return self.__dataset_of_podcasts

    @property
    def dataset_of_episodes(self):
        return self.__dataset_of_episodes

    @property
    def dataset_of_authors(self):
        return self.__dataset_of_authors

    @property
    def dataset_of_categories(self):
        return self.__dataset_of_categories

    @property
    def dataset_of_reviews(self):
        return self.__dataset_of_reviews