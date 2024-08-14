import csv
from pathlib import Path
from podcast.domainmodel.model import Podcast, Episode
from podcast.adapters.memory_repository import MemoryRepository


class CSVDataReader:
    def read_csv_file(self, filename: str):
        with open(filename, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)

            # Read column names of the CSV file
            column_names = next(reader)

            # Read remaining rows from the CSV file
            for row in reader:
                row = [item.strip() for item in row]
                yield row

    def load_podcasts_authors_categories(self, data_path: Path, repository: MemoryRepository):
        podcasts_filename = str(data_path / "podcasts.csv")
        for data_row in self.read_csv_file(podcasts_filename):
            podcast_id = int(data_row[0])
            podcast_title = data_row[1]
            image = data_row[2]
            description = data_row[3]
            language = data_row[4]
            categories = [category.strip() for category in data_row[5].split('|')]
            website = data_row[6]
            podcast_author = repository.add_or_get_author(data_row[7])
            itunes_id = int(data_row[8])
            new_podcast = Podcast(podcast_id, podcast_author, podcast_title, image, description, website,
                                  itunes_id, language)

            # add podcast to author's podcast list
            podcast_author.add_podcast(new_podcast)

            # add podcast to categories
            for category in categories:
                podcast_category = repository.add_or_get_category(category)
                new_podcast.add_category(podcast_category)

            # add podcast to the list for future access
            repository.add_podcast(new_podcast)

    # TODO: implement method to load episodes.csv
    def load_episodes(self, data_path: Path, repository: MemoryRepository):
        pass

    def populate_data(self, data_path: Path, repository: MemoryRepository):
        # Load podcasts, authors, and categories into the repository.
        self.load_podcasts_authors_categories(data_path, repository)

        # Load episodes into the repository.
        self.load_episodes(data_path, repository)
