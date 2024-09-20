import podcast.utilities.utilities
from podcast.browse import services as browse_services
from podcast.description import services as description_services
from podcast.home import services as home_services
from podcast.utilities import services as utilities_services
from podcast.user import services as user_services
from unittest.mock import patch


def test_get_podcast_by_page(in_memory_repo):
    dict = browse_services.get_podcasts_by_page(in_memory_repo, 1)
    assert len(dict['podcasts']) == 4
    assert repr(dict['podcasts'][3]) == "<Podcast 4: 'Tallin Messages' by Tallin Country Church>"
    assert repr(dict['podcasts'][2]) == "<Podcast 3: 'Onde Road - Radio Popolare' by Brian Denny>"
    assert dict['podcasts'][2].itunes_id == 568005832


def test_get_podcast_by_category(in_memory_repo):
    dict = browse_services.get_podcasts_by_category(in_memory_repo, 'Society & Culture', 1)
    assert len(dict['podcasts']) == 2
    assert dict['current_page'] == 1
    assert dict['has_next'] is False
    assert dict['has_previous'] is False
    assert dict['next_page'] == 1
    assert dict['previous_page'] == 1

    dict1 = browse_services.get_podcasts_by_category(in_memory_repo, 'Professional', 1)
    assert len(dict1['podcasts']) == 2
    assert dict['current_page'] == 1
    # Podcasts ordered alphabetically
    assert repr(dict1['podcasts'][0]) == "<Podcast 2: 'Brian Denny Radio' by Brian Denny>"
    assert repr(dict1['podcasts'][1]) == "<Podcast 1: 'D-Hour Radio Network' by D Hour Radio Network>"


def test_get_podcast_by_id(in_memory_repo):
    podcast = description_services.get_podcast_by_id(in_memory_repo, 1)
    podcast3 = description_services.get_podcast_by_id(in_memory_repo, 3)
    assert repr(podcast) == "<Podcast 1: 'D-Hour Radio Network' by D Hour Radio Network>"
    assert repr(podcast3) == "<Podcast 3: 'Onde Road - Radio Popolare' by Brian Denny>"


def test_get_random_podcasts_info(in_memory_repo):
    dict = home_services.get_random_podcasts_info(in_memory_repo, 3)
    assert len(dict) == 3
    dict1 = home_services.get_random_podcasts_info(in_memory_repo, 1)
    assert len(dict1) == 1
    dict2 = home_services.get_random_podcasts_info(in_memory_repo, 4)
    assert len(dict2) == 4
    dict3 = home_services.get_random_podcasts_info(in_memory_repo, 3)
    assert (dict3[0]['id'] == 1 or dict3[0]['id'] == 2 or dict3[0]['id'] == 3 or dict3[0]['id'] == 4)


def test_get_categories(in_memory_repo):
    categories = utilities_services.get_categories(in_memory_repo)
    assert len(categories) == 3
    # Category ordered alphabetically
    assert categories[0].name == "Comedy"
    assert categories[1].name == "Professional"
    assert categories[2].name == "Society & Culture"

def test_get_episode_by_id(in_memory_repo):
    episode1 = in_memory_repo.get_episode(1)
    episode2 = user_services.get_episode_by_id(in_memory_repo, 1)
    assert episode1 == episode2

def test_delete_review(in_memory_repo):
    in_memory_repo.add_user('test1', 'abcdE12')
    user1 = in_memory_repo.get_user('test1')
    podcast1 = in_memory_repo.get_podcast(1)
    in_memory_repo.add_review(podcast1, user1, 5, "Very good")
    user_services.delete_review(in_memory_repo, 1)
    assert len(user1.reviews) == 0

def test_in_playlist(in_memory_repo):
    in_memory_repo.add_user('new_user', 'passw0Rd')
    user1 = in_memory_repo.get_user('new_user')
    episode1 = in_memory_repo.get_episode(1)
    in_memory_repo.add_to_playlist('new_user', episode1)
    playlist1 = in_memory_repo.get_users_playlist('new_user')
    assert utilities_services.in_playlist(playlist1, episode1)

@patch('podcast.utilities.utilities.get_username')
def test_get_users_playlist(mock_get_username, in_memory_repo):
    mock_get_username.return_value = 'test_user'
    in_memory_repo.add_user('test_user', 'Abcde12')
    user_test = in_memory_repo.get_user('test_user')
    user_test.create_playlist('test_playlist')
    result_playlist = user_services.get_users_playlist(in_memory_repo)
    assert result_playlist.name == 'test_playlist'
    assert result_playlist.owner == user_test

@patch('podcast.utilities.utilities.get_username')
def test_get_and_remove_episodes_from_playlist(mock_get_username, in_memory_repo):
    mock_get_username.return_value = 'test_user1'
    in_memory_repo.add_user('test_user1', 'ABCDe12')
    user_test1 = in_memory_repo.get_user('test_user1')
    user_test1.create_playlist('test_playlist1')
    episode1 = in_memory_repo.get_episode(1)
    user_test1.playlist.add_episode(episode1)
    result_playlist = user_services.get_users_playlist(in_memory_repo)
    episodes = user_services.get_episodes_in_playlist(result_playlist)
    assert episodes[0] == in_memory_repo.get_episode(1)
    user_services.remove_from_playlist(in_memory_repo, episode1)
    assert len(result_playlist.episodes) == 0

@patch('podcast.utilities.utilities.get_username')
def test_get_user_reviews(mock_get_username, in_memory_repo):
    mock_get_username.return_value = 'test_user2'
    in_memory_repo.add_user('test_user2', 'ABCde12')
    user_test2 = in_memory_repo.get_user('test_user2')
    assert user_test2.reviews == in_memory_repo.get_users_reviews('test_user2')


# TODO: fix bugs
