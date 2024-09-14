from podcast.browse import services as browse_services
from podcast.description import services as description_services
from podcast.domainmodel.model import Podcast, Author, User, Review
from podcast.home import services as home_services
from podcast.utilities import services as utilities_services


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

def test_can_add_review(in_memory_repo):
    review_id = 10
    podcast1 = Podcast(1, Author(1, "test"), "Untitled", "", "", "", 1, "")
    user1 = User(1, "abcde", "Ab123456")
    podcast1 = Podcast(1, Author(1, "test"), "Untitled", "", "", "", 1, "")
    review = Review(1, podcast1, user1, 5, "Good podcast")
    description = "Good podcast"
    rating = 5
    description_services.add_review(review_id, podcast1, description, rating, user1, in_memory_repo)
    reviews_as_dict = description_services.get_reviews_for_podcast(1, in_memory_repo)
    assert next(
        (dictionary['review_content'] for dictionary in reviews_as_dict if dictionary['review_content'] == review_content),
        None)is not None

def test_get_reviews_for_podcast(in_memory_repo):
    reviews_as_dict = description_services.get_reviews_for_podcast(1, in_memory_repo)
    assert len(reviews_as_dict) == 2
    review_ids = [review['review_id'] for review in reviews_as_dict]
    review_ids = set(review_ids)
    assert 1 in review_ids and len(review_ids) == 1

