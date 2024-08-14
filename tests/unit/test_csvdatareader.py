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
    assert number_of_podcasts == 4  # Check that the query returned 4 Podcasts in the test file


def test_csv_data_reader_retrieve_podcast(in_memory_repo):
    podcast = in_memory_repo.get_podcast(1)
    # Check the first podcast properties have been read correctly
    assert podcast.title == "D-Hour Radio Network"
    assert podcast.image == "http://is3.mzstatic.com/image/thumb/Music118/v4/b9/ed/86/b9ed8603-d94b-28c5-5f95-8b7061bf22fa/source/600x600bb.jpg"
    assert len(podcast.categories) == 2
    assert podcast.website == "http://www.blogtalkradio.com/dhourshow"
    assert podcast.author.name == "D Hour Radio Network"
    assert podcast.itunes_id == 538283940


def test_csv_data_reader_retrieve_author_podcasts(in_memory_repo):
    author = in_memory_repo.get_podcast(2).author
    assert author.name == "Brian Denny"
    assert len(author.podcast_list) == 2  # Check that Author Brian Denny has two podcasts


def test_csv_data_reader_retrieve_categories_counts(in_memory_repo):
    categories = in_memory_repo.get_categories()
    assert len(categories) == 3  # Check that the query returned 3 Categories


def test_csv_data_reader_retrieve_category_podcasts(in_memory_repo):
    # Check that the first Category is Society & Culture
    category = in_memory_repo.get_categories()[0]
    assert category.name == "Society & Culture"

    # Check that the query returned 2 podcasts in Category Society & Culture
    podcast_ids_by_category = in_memory_repo.get_podcasts_ids_for_category(category.name)
    assert len(podcast_ids_by_category) == 2

    # Check that Podcast 1 and Podcast 3 are in Category Society & Culture
    podcasts = in_memory_repo.get_podcasts_by_id(podcast_ids_by_category)
    assert len(podcasts) == 2
    assert podcasts[0] == in_memory_repo.get_podcast(1)
    assert podcasts[1] == in_memory_repo.get_podcast(3)

