from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.domainmodel.model import Review, Podcast, User, Playlist, Episode, Category, Author
from podcast.adapters.repository import RepositoryException
from sqlalchemy.orm.exc import NoResultFound


def test_repository_can_add_and_get_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    podcast1 = Podcast(5, Author(1, "Shakespear"),"Untitled", "", "", "", 52, "")
    repo.add_podcast(podcast1)
    number_of_podcasts = repo.get_number_of_podcasts()
    assert number_of_podcasts == 5
    podcast = repo.get_podcast(5)
    assert podcast == podcast1
    podcast2 = repo.get_podcast(6)
    assert NoResultFound("Podcast 6 was not found.")
    assert podcast2 is None
    podcast2 = Podcast(6, Author(2, "BBC"), "News", "","","",41,"")
    repo.add_podcast(podcast2)
    assert repo.get_number_of_podcasts() == 6


def test_repository_can_get_podcasts_by_page(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    page_number_one = 1
    page_number_two = 2
    page_size = 3
    podcasts_page_one = repo.get_podcasts_by_page(page_number_one, page_size)
    podcasts_page_two = repo.get_podcasts_by_page(page_number_two, page_size)
    assert len(podcasts_page_one) == 3
    assert len(podcasts_page_two) == 1


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User(1, "TestUser", "TestUser1234")
    repo.add_user("TestUser", "TestUser1234")
    added_user = repo.get_user("TestUser")
    assert added_user == user


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user("prince")
    assert user is None


def test_repository_can_check_and_get_pages(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    current_page = 1
    page_size = 3
    assert repo.has_next_page(current_page, page_size) is True
    assert repo.has_previous_page(current_page) is False
    assert repo.get_next_page(current_page, page_size) == 2
    assert repo.get_previous_page(current_page) == 1


# TODO: MORE TESTING CASES
