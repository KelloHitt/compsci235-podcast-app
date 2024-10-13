from sqlalchemy.orm.exc import NoResultFound

from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.domainmodel.model import Podcast, User, Episode, Author


def test_database_repository_can_add_and_get_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    podcast1 = Podcast(5, Author(1, "Shakespear"), "Untitled", "", "", "", 52, "")
    repo.add_podcast(podcast1)
    number_of_podcasts = repo.get_number_of_podcasts()
    assert number_of_podcasts == 5
    podcast = repo.get_podcast(5)
    assert podcast == podcast1
    podcast2 = repo.get_podcast(6)
    assert NoResultFound("Podcast 6 was not found.")
    assert podcast2 is None
    podcast2 = Podcast(6, Author(2, "BBC"), "News", "", "", "", 41, "")
    repo.add_podcast(podcast2)
    assert repo.get_number_of_podcasts() == 6


def test_database_repository_can_get_podcasts_by_id_list(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    podcasts_by_id = repo.get_podcasts_by_id([1, 2, 3, 4])
    assert len(podcasts_by_id) == 4


def test_database_repository_can_get_podcasts_by_page(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    page_number_one = 1
    page_number_two = 2
    page_size = 3
    podcasts_page_one = repo.get_podcasts_by_page(page_number_one, page_size)
    podcasts_page_two = repo.get_podcasts_by_page(page_number_two, page_size)
    assert len(podcasts_page_one) == 3
    assert len(podcasts_page_two) == 1


def test_database_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User(1, "TestUser", "TestUser1234")
    repo.add_user("TestUser", "TestUser1234")
    added_user = repo.get_user("TestUser")
    assert added_user == user


def test_database_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user("prince")
    assert user is None


def test_database_repository_can_check_and_get_pages(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    current_page = 1
    page_size = 3
    assert repo.has_next_page(current_page, page_size) is True
    assert repo.has_previous_page(current_page) is False
    assert repo.get_next_page(current_page, page_size) == 2
    assert repo.get_previous_page(current_page) == 1


def test_database_repository_can_retrieve_episodes(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    number_of_episodes = repo.get_number_of_episodes()
    assert number_of_episodes == 4


def test_database_repository_can_retrieve_categories(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    categories = repo.get_categories()
    assert len(categories) == 3
    assert categories[0].name == "Comedy"


def test_database_repository_get_podcasts_ids_for_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    list_of_ids = repo.get_podcasts_ids_for_category("Comedy")
    assert len(list_of_ids) == 2


def test_database_repository_get_episode(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    episode = repo.get_episode(1)
    assert episode.id == 1
    assert episode.title == "Choir"
    assert episode.description == "Choir"
    assert episode.date == "2017-12-01 10:03:18"


def test_database_repository_add_episode(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    podcast1 = Podcast(5, Author(1, "Shakespear"), "Untitled", "", "", "", 52, "")
    repo.add_podcast(podcast1)
    episode = Episode(5, podcast1, "Untitled", "", "", 20, "2007-08-09::")
    repo.add_episode(episode)
    assert repo.get_number_of_episodes() == 5


def test_database_repository_retrieve_category_podcasts(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    category = repo.get_categories()[1]
    assert category.name == "Professional"

    # Check that the query returned 2 podcasts in Category Professional
    podcast_ids_by_category = repo.get_podcasts_ids_for_category("Professional")
    assert podcast_ids_by_category == [1, 2]


def test_database_repository_can_add_to_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    episode1 = repo.get_episode(1)
    repo.add_user('test1', 'abcdE123')
    user1 = repo.get_user('test1')
    user1.create_playlist('playlist1')
    repo.add_to_playlist('test1', episode1)
    assert len(user1.playlist.episodes) == 1


def test_repository_can_make_and_add_to_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    episode1 = repo.get_episode(2)
    repo.add_user('test2', 'abcdE123')
    user1 = repo.get_user('test2')
    repo.add_to_playlist('test2', episode1)
    assert user1.playlist.episodes == [episode1]


def test_repository_can_get_users_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user('test3', 'abcdE123')
    user1 = repo.get_user('test3')
    user1.create_playlist('playlist1')
    assert user1.playlist == repo.get_users_playlist('test3')


def test_repository_can_make_and_get_users_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user('test4', 'abcdE123')
    user1 = repo.get_user('test4')
    playlist1 = repo.get_users_playlist('test4')
    assert user1.playlist == playlist1


def test_database_repository_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user('Bobby', 'Bobby1234')
    user = repo.get_user('Bobby')
    author = Author(6, 'Haku')
    podcast = Podcast(10, author, "Demon Slayer", "", "", "", 500, "English")
    repo.add_review(podcast, user, 5, "Interesting")
    assert user.reviews[0].id == 1
    assert (("<Review 1 made by Bobby for podcast 'Demon Slayer' with a rating of 5 and a description of Interesting>")
            == repr(podcast.reviews[0]))


def test_database_repository_get_users_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user('Bobby', 'Bobby1234')
    user = repo.get_user('Bobby')
    author = Author(6, 'Haku')
    podcast1 = Podcast(10, author, "Demon Slayer", "", "", "", 500, "English")
    repo.add_review(podcast1, user, 5, "Interesting")
    podcast2 = Podcast(11, author, "Mugen Train", "", "", "", 40, "English")
    repo.add_review(podcast2, user, 1, "Disappointing")
    reviews = repo.get_users_reviews('Bobby')
    assert user.reviews[0].id == 1
    assert user.reviews[1].id == 2
    assert len(reviews) == 2


def test_database_repository_delete_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user('Bobby', 'Bobby1234')
    user = repo.get_user('Bobby')
    author = Author(6, 'Haku')
    podcast1 = Podcast(10, author, "Demon Slayer", "", "", "", 500, "English")
    repo.add_review(podcast1, user, 5, "Interesting")
    podcast2 = Podcast(11, author, "Mugen Train", "", "", "", 40, "English")
    repo.add_review(podcast2, user, 1, "Disappointing")
    reviews = repo.get_users_reviews('Bobby')
    assert user.reviews[0].id == 1
    assert user.reviews[1].id == 2
    assert len(reviews) == 2
    repo.delete_review(1)
    assert len(podcast1.reviews) == 0
    assert len(user.reviews) == 1
    repo.delete_review(2)
    assert len(podcast2.reviews) == 0
    assert len(user.reviews) == 0


def test_repository_get_podcasts_by_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    podcasts = repo.get_podcasts_by_category('Comedy')
    assert 2 == len(podcasts)
    assert "<Podcast 2: 'Brian Denny Radio' by Brian Denny>" == repr(podcasts[0])
    assert "<Podcast 4: 'Tallin Messages' by Tallin Country Church>" == repr(podcasts[1])


def test_repository_get_podcasts_by_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    podcasts = repo.get_podcasts_by_author('Brian')
    assert "<Podcast 2: 'Brian Denny Radio' by Brian Denny>" == repr(podcasts[0])
    assert "<Podcast 3: 'Onde Road - Radio Popolare' by Brian Denny>" == repr(podcasts[1])


def test_repository_get_podcasts_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    podcasts = repo.get_podcasts_by_title('Messages')
    assert "<Podcast 4: 'Tallin Messages' by Tallin Country Church>" == repr(podcasts[0])


def test_repository_get_episodes_by_language(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    podcasts = repo.get_podcasts_by_language("English")
    assert "<Podcast 1: 'D-Hour Radio Network' by D Hour Radio Network>" == repr(podcasts[0])
