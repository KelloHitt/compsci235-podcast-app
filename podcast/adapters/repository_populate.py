from pathlib import Path

from podcast.adapters.repository import AbstractRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader


def populate_data(repo: AbstractRepository, data_path: Path):
    reader = CSVDataReader()
    reader.load_podcasts_authors_categories(data_path)
    reader.load_episodes(data_path)

    podcasts = reader.dataset_of_podcasts
    authors = reader.dataset_of_authors
    categories = reader.dataset_of_categories
    episodes = reader.dataset_of_episodes
    reviews = reader.dataset_of_reviews

    for author in authors.values():
        repo.add_author(author)

    for podcast in podcasts:
        repo.add_podcast(podcast)

    for category in categories.values():
        repo.add_category(category)

    for episode in episodes:
        repo.add_episode(episode)

    for review in reviews:
        repo.add_review(review.content, review.rating, review.podcast, review.reviewer)
