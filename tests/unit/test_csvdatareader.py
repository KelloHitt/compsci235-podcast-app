from pathlib import Path

import pytest

from podcast.adapters.datareader.csvdatareader import CSVDataReader


@pytest.fixture
def data_path() -> Path:
    data_path = Path(__file__).parent.parent / "data"
    return data_path


@pytest.fixture
def csv_reader() -> CSVDataReader:
    csv_reader = CSVDataReader()
    return csv_reader


def test_csv_data_reader_load_podcasts_authors_categories(data_path: Path, csv_reader: CSVDataReader):
    csv_reader.load_podcasts_authors_categories(data_path)
    assert len(csv_reader.dataset_of_podcasts) == 4
    assert len(csv_reader.dataset_of_authors) == 3
    assert len(csv_reader.dataset_of_categories) == 3


def test_csv_data_reader_load_episodes(data_path: Path, csv_reader: CSVDataReader):
    csv_reader.load_podcasts_authors_categories(data_path)
    csv_reader.load_episodes(data_path)
    assert len(csv_reader.dataset_of_podcasts) == 4


def test_csv_data_reader_add_or_get_author(data_path: Path, csv_reader: CSVDataReader):
    csv_reader.load_podcasts_authors_categories(data_path)
    author_name = "Shakespear"
    author1 = csv_reader.add_or_get_author(author_name)
    author2 = csv_reader.add_or_get_author("")
    author3 = csv_reader.add_or_get_author(author_name)
    assert csv_reader.dataset_of_authors[author_name] == author1
    assert csv_reader.dataset_of_authors["Unknown"] == author2
    assert author3 == author1
    assert len(csv_reader.dataset_of_authors) == 5


def test_csv_data_reader_add_or_get_category(data_path: Path, csv_reader: CSVDataReader):
    csv_reader.load_podcasts_authors_categories(data_path)
    category_name = "Education"
    category1 = csv_reader.add_or_get_category(category_name)
    category2 = csv_reader.add_or_get_category(category_name)
    assert category2 == category1
    assert len(csv_reader.dataset_of_categories) == 4


def test_csv_data_reader_get_podcast_by_id(data_path: Path, csv_reader: CSVDataReader):
    csv_reader.load_podcasts_authors_categories(data_path)

    podcast1 = csv_reader.get_podcast_by_id(1)
    assert podcast1.title == "D-Hour Radio Network"
    assert podcast1.image == "http://is3.mzstatic.com/image/thumb/Music118/v4/b9/ed/86/b9ed8603-d94b-28c5-5f95-8b7061bf22fa/source/600x600bb.jpg"
    assert len(podcast1.categories) == 2
    assert podcast1.website == "http://www.blogtalkradio.com/dhourshow"
    assert podcast1.author.name == "D Hour Radio Network"
    assert podcast1.itunes_id == 538283940

    podcast2 = csv_reader.get_podcast_by_id(2)
    author = podcast2.author
    assert author.name == "Brian Denny"
    assert len(author.podcast_list) == 2

    podcast3 = csv_reader.get_podcast_by_id(404)
    assert podcast3 is None
