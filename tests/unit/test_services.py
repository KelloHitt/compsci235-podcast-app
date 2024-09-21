from unittest.mock import patch
import pytest
from podcast.browse import services as browse_services
from podcast.description import services as description_services
from podcast.home import services as home_services
from podcast.user import services as user_services
from podcast.utilities import services as utilities_services
from podcast.authentication import services as authentication_services
from  podcast.authentication.services import AuthenticationException
from podcast.domainmodel.model import Podcast, Author, Episode, User
from podcast.search import services as search_services


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


# TODO: test authentication blueprint services - Venus

def test_add_valid_user(in_memory_repo):
    user_name1 = 'Cool'
    password1 = 'ahjke45'
    authentication_services.add_user(user_name1, password1, in_memory_repo)
    user_as_dict = authentication_services.get_user(user_name1, in_memory_repo)
    assert user_as_dict['username'] == user_name1
    assert user_as_dict['password'].startswith('scrypt:32768')

def test_add_invalid_user_with_existing_username(in_memory_repo):
    user_name1 = 'Cool'
    password1 = 'ahjke45'
    user_name2 = 'Cool'
    password2 = 'ahjke45'
    authentication_services.add_user(user_name1, password1, in_memory_repo)
    with pytest.raises(authentication_services.NameNotUniqueException):
        authentication_services.add_user(user_name2, password2, in_memory_repo)

def test_authentication_of_valid_user(in_memory_repo):
    user_name = 'blikeCole'
    password = '45hjdidh'
    authentication_services.add_user(user_name, password, in_memory_repo)
    try:
        authentication_services.authenticate_user(user_name, password, in_memory_repo)
    except AuthenticationException:
        assert False

def test_authentication_with_invalid_credentials(in_memory_repo):
    user_name = 'blikeCole'
    password = '45hjdidh'
    authentication_services.add_user(user_name, password, in_memory_repo)
    with pytest.raises(authentication_services.AuthenticationException):
        authentication_services.authenticate_user(user_name, 'jdidh45', in_memory_repo)

# TODO: test added functions in description/services.py - Venus

@patch('podcast.utilities.utilities.get_username')
def test_add_to_playlist(mock_get_username, in_memory_repo):
    mock_get_username.return_value = 'test_user3'
    in_memory_repo.add_user('test_user3', 'AbCde75')
    author = Author(1, "Joe")
    podcast = Podcast(1, author, "The Seven Wonders Of The World", "Tune in into this great podcast", "https://www.twinkl.co.nz/teaching-wiki/seven-wonders-of-the-world", "English")
    episode = Episode(1, podcast, "1st wonder of the world", "http://api.spreaker.com/download/episode/13479186/comixology_runaways_and_star_trek.mp3", "Tune in to find more", 3, "2017-12-01 13:00:05+00")
    description_services.add_to_playlist(in_memory_repo, episode)
    assert episode == (description_services.get_playlist(in_memory_repo).episodes)[0]

@patch('podcast.utilities.utilities.get_username')
def test_remove_from_playlist(mock_get_username, in_memory_repo):
    mock_get_username.return_value = 'test_user3'
    in_memory_repo.add_user('test_user3', 'AbCde75')
    author = Author(1, "Joe")
    podcast = Podcast(1, author, "The Seven Wonders Of The World", "Tune in into this great podcast",
                      "https://www.twinkl.co.nz/teaching-wiki/seven-wonders-of-the-world", "English")
    episode = Episode(1, podcast, "1st wonder of the world",
                      "http://api.spreaker.com/download/episode/13479186/comixology_runaways_and_star_trek.mp3",
                      "Tune in to find more", 3, "2017-12-01 13:00:05+00")
    description_services.add_to_playlist(in_memory_repo, episode)
    description_services.remove_from_playlist(in_memory_repo, episode)
    assert "<Playlist 1 'Test_User3's Playlist': Owned by test_user3>" == repr(description_services.get_playlist(in_memory_repo))
    assert [] == (description_services.get_playlist(in_memory_repo)).episodes


@patch('podcast.utilities.utilities.get_username')
def test_get_user_by_username(mock_get_username, in_memory_repo):
    mock_get_username.return_value = 'blaire'
    in_memory_repo.add_user('blaire', 'hijk345')
    assert '<User 1: blaire>' == repr(description_services.get_user_by_username(in_memory_repo, 'blaire'))


def test_add_review(in_memory_repo):
    user = User(1, 'Jill', 'kit675')
    author = Author(1, 'Alice')
    podcast = Podcast(1, author, 'The rise of the phoenix', None, 'Tune in to find out more', 'https://en.wikipedia.org/wiki/Phoenix_(mythology)', None, 'English')
    description = 'Wonderful and insightful podcast'
    rating = 5
    description_services.add_review(in_memory_repo, podcast, user, rating, description)
    assert repr(user.reviews[0]) == "<Review 1 made by Jill for podcast 'The rise of the phoenix' with a rating of 5 and a description of Wonderful and insightful podcast>"

def test_add_invalid_review(in_memory_repo):
    user = None
    author = Author(1, 'Alice')
    podcast = Podcast(1, author, 'The rise of the phoenix', None, 'Tune in to find out more',
                      'https://en.wikipedia.org/wiki/Phoenix_(mythology)', None, 'English')
    description = 'Wonderful and insightful podcast'
    rating = 5
    with pytest.raises(ValueError):
        description_services.add_review(in_memory_repo, podcast, user, rating, description)



# # TODO: test methods in search/services.py - Venus
# def test_get_podcasts_filtered_by_category(in_memory_repo):
#     search_field = 'category'
#     search_query = 'comedy'
#     assert 2 == len(search_services.get_podcasts_filtered(in_memory_repo, search_field, search_query))
#     assert "<Podcast 2: 'Brian Denny Radio' by Brian Denny>" == repr((search_services.get_podcasts_filtered(in_memory_repo, search_field, search_query))[0])
#     assert "<Podcast 4: 'Tallin Messages' by Tallin Country Church>" == repr(((search_services.get_podcasts_filtered(in_memory_repo, search_field, search_query))[1]))
#
# def test_get_podcasts_filtered_by_title(in_memory_repo):
#     search_field = 'category'
#     search_query = 'comedy'