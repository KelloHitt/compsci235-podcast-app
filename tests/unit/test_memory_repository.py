from podcast.domainmodel.model import Podcast, Author, Episode, User, Playlist


def test_memory_repository_can_retrieve_podcasts(in_memory_repo):
    number_of_podcasts = in_memory_repo.get_number_of_podcasts()
    assert number_of_podcasts == 4


def test_memory_repository_can_retrieve_episodes(in_memory_repo):
    number_of_episodes = in_memory_repo.get_number_of_episodes()
    assert number_of_episodes == 4


def test_memory_repository_can_retrieve_categories(in_memory_repo):
    categories = in_memory_repo.get_categories()
    assert len(categories) == 3
    assert categories[0].name == "Comedy"


def test_memory_repository_add_podcast(in_memory_repo):
    podcast1 = in_memory_repo.get_podcast(1)
    in_memory_repo.add_podcast(podcast1)
    assert in_memory_repo.get_number_of_podcasts() == 4
    podcast2 = Podcast(5, Author(5, "Shakespear"), "Untitled", "", "", "", 52, "")
    in_memory_repo.add_podcast(podcast2)
    assert in_memory_repo.get_number_of_podcasts() == 5


def test_memory_repository_get_podcast(in_memory_repo):
    podcast1 = in_memory_repo.get_podcast(1)
    assert podcast1.title == "D-Hour Radio Network"
    podcast2 = in_memory_repo.get_podcast(10)
    assert podcast2 is None


def test_memory_repository_get_podcasts_by_id_list(in_memory_repo):
    podcasts = in_memory_repo.get_podcasts_by_id([1, 2, 3, 4])
    assert len(podcasts) == 4


def test_memory_repository_get_podcasts_by_page(in_memory_repo):
    page_number_one = 1
    page_number_two = 2
    page_size = 3
    podcasts_page_one = in_memory_repo.get_podcasts_by_page(page_number_one, page_size)
    podcasts_page_two = in_memory_repo.get_podcasts_by_page(page_number_two, page_size)
    assert len(podcasts_page_one) == 3
    assert len(podcasts_page_two) == 1


def test_memory_repository_get_podcasts_ids_for_category(in_memory_repo):
    list_of_ids = in_memory_repo.get_podcasts_ids_for_category("Comedy")
    assert len(list_of_ids) == 2


def test_memory_repository_has_next_page(in_memory_repo):
    current_page = 2
    page_size = 2
    has_next_page = in_memory_repo.has_next_page(current_page, page_size)
    assert has_next_page is False


def test_memory_repository_has_previous_page(in_memory_repo):
    current_page = 2
    has_previous_page = in_memory_repo.has_previous_page(current_page)
    assert has_previous_page is True


def test_memory_repository_get_next_page(in_memory_repo):
    current_page = 1
    page_size = 2
    next_page = in_memory_repo.get_next_page(current_page, page_size)
    assert next_page == 2


def test_memory_repository_get_previous_page(in_memory_repo):
    current_page = 2
    previous_page = in_memory_repo.get_previous_page(current_page)
    assert previous_page == 1


def test_memory_repository_get_episode(in_memory_repo):
    episode = in_memory_repo.get_episode(1)
    assert episode.id == 1
    assert episode.title == "Choir"
    assert episode.url == "https://anchor.fm/s/12e5a58/podcast/download/66596/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fanchor-data%2Fstationexports%2Fpodcasts%2FChoir-140563529b196.m4a"
    assert episode.length == 266
    assert episode.description == "Choir"
    assert episode.date == "2017-12-01 10:03:18"


def test_memory_repository_add_episode(in_memory_repo):
    podcast = in_memory_repo.get_podcast(1)
    episode = Episode(5, podcast, "Untitled", "", "", 20, "2007-08-09::")
    in_memory_repo.add_episode(episode)
    assert in_memory_repo.get_number_of_episodes() == 5
    assert in_memory_repo.get_episode(5) == episode


def test_csv_data_reader_retrieve_category_podcasts(in_memory_repo):
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


def test_repository_can_add_and_retrieve_a_user(in_memory_repo):
    user = User(1, "dave", "123456789")
    in_memory_repo.add_user("dave", "123456789")
    added_user = in_memory_repo.get_user("dave")
    assert added_user == user


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user("prince")
    assert user is None


def test_repository_can_add_to_preexisting_playlist(in_memory_repo):
    episode1 = in_memory_repo.get_episode(1)
    in_memory_repo.add_user('test1', 'abcdE12')
    user1 = in_memory_repo.get_user('test1')
    user1.create_playlist('playlist1')
    in_memory_repo.add_to_playlist('test1', episode1)
    assert len(user1.playlist.episodes) == 1


def test_repository_can_make_and_add_to_playlist(in_memory_repo):
    episode1 = in_memory_repo.get_episode(2)
    in_memory_repo.add_user('test2', 'abcdE12')
    user1 = in_memory_repo.get_user('test2')
    in_memory_repo.add_to_playlist('test2', episode1)
    assert len(user1.playlist.episodes) == 1


def test_repository_can_get_users_preexisting_playlist(in_memory_repo):
    in_memory_repo.add_user('test3', 'abcdE12')
    user1 = in_memory_repo.get_user('test3')
    user1.create_playlist('playlist1')
    assert user1.playlist == in_memory_repo.get_users_playlist('test3')


def test_repository_can_make_and_get_users_playlist(in_memory_repo):
    in_memory_repo.add_user('test4', 'abcdE12')
    user1 = in_memory_repo.get_user('test4')
    playlist1 = in_memory_repo.get_users_playlist('test4')
    assert user1.playlist == playlist1


def test_repository_get_podcasts_by_category(in_memory_repo):
    podcasts = in_memory_repo.get_podcasts_by_category('comedy')
    assert 2 == len(podcasts)
    assert "<Podcast 2: 'Brian Denny Radio' by Brian Denny>" == repr(podcasts[0])
    assert "<Podcast 4: 'Tallin Messages' by Tallin Country Church>" == repr(podcasts[1])


def test_repository_get_podcasts_by_author(in_memory_repo):
    podcasts = in_memory_repo.get_podcasts_by_author('Brian')
    assert "<Podcast 2: 'Brian Denny Radio' by Brian Denny>" == repr(podcasts[0])
    assert "<Podcast 3: 'Onde Road - Radio Popolare' by Brian Denny>" == repr(podcasts[1])


def test_repository_get_podcasts_by_title(in_memory_repo):
    podcasts = in_memory_repo.get_podcasts_by_title('Messages')
    assert "<Podcast 4: 'Tallin Messages' by Tallin Country Church>" == repr(podcasts[0])


def test_repository_add_review(in_memory_repo):
    user = User(1, 'Claire', 'nice347')
    author = Author(1, 'Joe')
    podcast = Podcast(1, author, "The Seven Wonders Of The World", "Tune in into this great podcast",
                      "","https://www.twinkl.co.nz/teaching-wiki/seven-wonders-of-the-world", 5,"English")
    in_memory_repo.add_review(podcast, user, 2, "sort of boring")
    assert user.reviews[0].id == 1
    assert ("<Review 1 made by Claire for podcast 'The Seven Wonders Of The World' with a rating of 2 and a "
            "description of sort of boring>") == repr(user.reviews[0])


def test_repository_get_users_reviews(in_memory_repo):
    in_memory_repo.add_user('Claire', 'nice347')
    user = in_memory_repo.get_user('Claire')
    author = Author(1, 'Joe')
    podcast = Podcast(1, author, "The Seven Wonders Of The World", "Tune in into this great podcast",
                      "","https://www.twinkl.co.nz/teaching-wiki/seven-wonders-of-the-world", 5,"English")
    in_memory_repo.add_review(podcast, user, 2, "sort of boring")
    podcast1 = Podcast(2, author, "Productivity", None, "Tune in into this great podcast",
                       "https://www.twinkl.co.nz/teaching-wiki/seven-wonders-of-the-world", 40,"English")
    in_memory_repo.add_review(podcast1, user, 2, "better than the seven wonders of the world podcast")
    reviews = in_memory_repo.get_users_reviews('Claire')
    assert len(reviews) == 2


def test_repository_delete_review(in_memory_repo):
    in_memory_repo.add_user('Bob', 'cars23')
    user = in_memory_repo.get_user('Bob')
    author = Author(1, 'Joe')
    podcast = Podcast(1, author, "The Seven Wonders Of The World", None, "Tune in into this great podcast",
                      "https://www.twinkl.co.nz/teaching-wiki/seven-wonders-of-the-world", 50,"English")
    in_memory_repo.add_review(podcast, user, 5, 'Intriguing!')
    assert len(podcast.reviews) == 1
    assert len(user.reviews) == 1
    in_memory_repo.delete_review(1)
    assert len(podcast.reviews) == 0
    assert len(user.reviews) == 0
