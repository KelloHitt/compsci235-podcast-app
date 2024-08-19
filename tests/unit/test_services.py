import pytest
from pathlib import Path
from podcast.browse import services as browse_services
from podcast.description import services as description_services
from podcast.home import services as home_services
from podcast.utilities import services as utilities_services
from podcast.adapters.memory_repository import MemoryRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader
@pytest.fixture
def in_memory_repo() -> MemoryRepository:
    repository = MemoryRepository()
    data_path = Path("./tests/data/")
    csv_data_reader = CSVDataReader()
    csv_data_reader.populate_data(data_path, repository)
    return repository
# TODO: Test Browse services

def test_get_podcast_by_page(in_memory_repo):
    dict = browse_services.get_podcasts_by_page(in_memory_repo, 1)
    assert len(dict['podcasts']) == 4
    assert repr(dict['podcasts'][3]) == "<Podcast 4: 'Tallin Messages' by Tallin Country Church>"
    print("Get podcasts by page", dict['podcasts'])
    assert repr(dict['podcasts'][2]) == "<Podcast 3: 'Onde Road - Radio Popolare' by Brian Denny>"
    assert dict['podcasts'][2].itunes_id == 568005832

def test_get_podcast_by_category(in_memory_repo):
    dict = browse_services.get_podcasts_by_category(in_memory_repo, 'Society & Culture', 1)
    assert len(dict['podcasts']) == 2
    assert dict['current_page'] == 1
    assert dict['has_next'] == False

    dict1 = browse_services.get_podcasts_by_category(in_memory_repo, 'Professional', 1)
    assert len(dict1['podcasts']) == 2
    assert dict['current_page'] == 1
    assert repr(dict1['podcasts'][0])== "<Podcast 1: 'D-Hour Radio Network' by D Hour Radio Network>"


# TODO: Test Description services
def test_get_podcast_by_id(in_memory_repo):
    podcast = description_services.get_podcast_by_id(in_memory_repo, 1)
    podcast3 = description_services.get_podcast_by_id(in_memory_repo, 3)
    assert repr(podcast) == "<Podcast 1: 'D-Hour Radio Network' by D Hour Radio Network>"
    assert repr(podcast3) == "<Podcast 3: 'Onde Road - Radio Popolare' by Brian Denny>"

# TODO: Test Home services
def test_get_random_podcasts_info(in_memory_repo):
   dict =  home_services.get_random_podcasts_info(in_memory_repo, 3)
   assert len(dict) == 3
   dict1 = home_services.get_random_podcasts_info(in_memory_repo, 1)
   assert len(dict1) == 1
   dict2 = home_services.get_random_podcasts_info(in_memory_repo, 4)
   assert len(dict2) == 4
   dict3 = home_services.get_random_podcasts_info(in_memory_repo, 3)
   print(dict3)
   assert (dict3[0]['id'] == 1 or dict3[0]['id'] == 2 or dict3[0]['id'] == 3 or dict3[0]['id'] == 4)


# TODO: Test Utilities services
def test_get_categories(in_memory_repo):
    categories = utilities_services.get_categories(in_memory_repo)
    print("Utilities: ", categories)
    assert  len(categories) == 3
    for category in categories:
        assert (category.name == "Comedy" or category.name == "Professional" or category.name == "Society & Culture")