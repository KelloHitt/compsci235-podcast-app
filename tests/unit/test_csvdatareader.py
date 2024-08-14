import pytest
from pathlib import Path
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.memory_repository import MemoryRepository


@pytest.fixture
def in_memory_repo() -> MemoryRepository:
    repository = MemoryRepository()
    data_path = Path("../data/")
    csv_data_reader = CSVDataReader()
    csv_data_reader.populate_data(data_path, repository)
    return repository


def test_csv_data_reader_retrieve_podcasts_counts(in_memory_repo):
    number_of_podcasts = in_memory_repo.get_number_of_podcasts()
    assert number_of_podcasts == 4  # Check that the query returned 4 Podcasts.


def test_csv_data_reader_retrieve_podcast(in_memory_repo):
    podcast = in_memory_repo.get_podcast(1)
    assert podcast.title == "D-Hour Radio Network"  # Check the first podcast title is D-Hour Radio Network
    assert podcast.author.name == "D Hour Radio Network"  # Check the first podcast author is D Hour Radio Network

def test_csv_data_reader_retrieve_author_podcasts(in_memory_repo):
    # TODO: test authors can have podcasts assigned to their list
    pass


# TODO: test categories can have podcasts

