import pytest
from pathlib import Path
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.memory_repository import MemoryRepository


@pytest.fixture
def in_memory_repo() -> MemoryRepository:
    repository = MemoryRepository()
    data_path = Path("./tests/data/")
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
    category = in_memory_repo.get_categories()[-1]
    assert category.name == "Society & Culture"

    # Check that the query returned 2 podcasts in Category Society & Culture
    podcast_ids_by_category = in_memory_repo.get_podcasts_ids_for_category(category.name)
    assert len(podcast_ids_by_category) == 2

    # Check that Podcast 1 and Podcast 3 are in Category Society & Culture
    podcasts = in_memory_repo.get_podcasts_by_id(podcast_ids_by_category)
    assert len(podcasts) == 2
    assert podcasts[0] == in_memory_repo.get_podcast(1)
    assert podcasts[1] == in_memory_repo.get_podcast(3)

def test_csv_data_reader_retrieve_number_of_episodes(in_memory_repo):
    number_of_episodes = in_memory_repo.get_number_of_episodes()
    assert number_of_episodes == 4

def test_csv_data_reader_retrieve_episode(in_memory_repo):
    episode = in_memory_repo.get_episode(7)
    # Check the episode with id 7 attributes have been read correctly
    assert episode.title == "Choir"
    assert episode.id == 7
    assert episode.url == "https://anchor.fm/s/12e5a58/podcast/download/66596/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fanchor-data%2Fstationexports%2Fpodcasts%2FChoir-140563529b196.m4a"
    assert episode.length == 266
    assert episode.description == "Choir"
    assert episode.date == "2017-12-01 10:03:18"
    if episode.podcast != None:
        assert episode.podcast.id == 27

    episode1 = in_memory_repo.get_episode(9)
    assert episode1.title == "Caller Of The Week Part 2."
    assert episode1.id == 9
    assert episode1.url == "https://post.futurimedia.com/wheb/playlist/2/615.m4a"
    assert episode1.length == 332
    assert episode1.description == "The best of Greg & The Morning Buzz. Listen weekdays 5:30am to 10am."
    assert episode1.date == "2017-12-01 14:43:49"
    if episode.podcast != None:
        assert episode1.podcast.id == 404

def test_csv_data_reader_get_number_of_episodes(in_memory_repo):
    number_of_podcasts = in_memory_repo.get_number_of_episodes()
    assert number_of_podcasts == 4

def test_csv__datareader_retrieve_episode_podcast_id(in_memory_repo):
    episode = in_memory_repo.get_episode(10)
    if episode.podcast != None:
        assert episode.podcast.id == 404












