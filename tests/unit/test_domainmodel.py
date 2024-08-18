import pytest
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode
from podcast.adapters.datareader.csvdatareader import CSVDataReader


def test_author_initialization():
    author1 = Author(1, "Brian Denny")
    assert repr(author1) == "<Author 1: Brian Denny>"
    assert author1.name == "Brian Denny"

    with pytest.raises(ValueError):
        author2 = Author(2, "")

    with pytest.raises(ValueError):
        author3 = Author(3, 123)

    author4 = Author(4, " USA Radio   ")
    assert author4.name == "USA Radio"

    author4.name = "Jackson Mumey"
    assert repr(author4) == "<Author 4: Jackson Mumey>"


def test_author_eq():
    author1 = Author(1, "Author A")
    author2 = Author(1, "Author A")
    author3 = Author(3, "Author B")
    assert author1 == author2
    assert author1 != author3
    assert author3 != author2
    assert author3 == author3


def test_author_lt():
    author1 = Author(1, "Jackson Mumey")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    assert author1 < author2
    assert author2 > author3
    assert author1 < author3
    author_list = [author3, author2, author1]
    assert sorted(author_list) == [author1, author3, author2]


def test_author_hash():
    authors = set()
    author1 = Author(1, "Doctor Squee")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    authors.add(author1)
    authors.add(author2)
    authors.add(author3)
    assert len(authors) == 3
    assert repr(
        sorted(authors)) == "[<Author 1: Doctor Squee>, <Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"
    authors.discard(author1)
    assert repr(sorted(authors)) == "[<Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"


def test_author_name_setter():
    author = Author(1, "Doctor Squee")
    author.name = "   USA Radio  "
    assert repr(author) == "<Author 1: USA Radio>"

    with pytest.raises(ValueError):
        author.name = ""

    with pytest.raises(ValueError):
        author.name = 123


def test_category_initialization():
    category1 = Category(1, "Comedy")
    assert repr(category1) == "<Category 1: Comedy>"
    category2 = Category(2, " Christianity ")
    assert repr(category2) == "<Category 2: Christianity>"

    with pytest.raises(ValueError):
        category3 = Category(3, 300)

    category5 = Category(5, " Religion & Spirituality  ")
    assert category5.name == "Religion & Spirituality"

    with pytest.raises(ValueError):
        category1 = Category(4, "")


def test_category_name_setter():
    category1 = Category(6, "Category A")
    assert category1.name == "Category A"

    with pytest.raises(ValueError):
        category1 = Category(7, "")

    with pytest.raises(ValueError):
        category1 = Category(8, 123)


def test_category_eq():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 == category1
    assert category1 != category2
    assert category2 != category3
    assert category1 != "9: Adventure"
    assert category2 != 105


def test_category_hash():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    category_set = set()
    category_set.add(category1)
    category_set.add(category2)
    category_set.add(category3)
    assert sorted(category_set) == [category1, category2, category3]
    category_set.discard(category2)
    category_set.discard(category1)
    assert sorted(category_set) == [category3]


def test_category_lt():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 < category2
    assert category2 < category3
    assert category3 > category1
    category_list = [category3, category2, category1]
    assert sorted(category_list) == [category1, category2, category3]


# Fixtures to reuse in multiple tests
@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")


@pytest.fixture
def my_podcast(my_author):
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")


@pytest.fixture
def my_user():
    return User(1, "Shyamli", "pw12345")


@pytest.fixture
def my_subscription(my_user, my_podcast):
    return PodcastSubscription(1, my_user, my_podcast)


def test_podcast_initialization():
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    assert podcast1.id == 2
    assert podcast1.author == author1
    assert podcast1.title == "My First Podcast"
    assert podcast1.description == ""
    assert podcast1.website == ""

    assert repr(podcast1) == "<Podcast 2: 'My First Podcast' by Doctor Squee>"

    with pytest.raises(ValueError):
        podcast3 = Podcast(-123, "Todd Clayton")

    podcast4 = Podcast(123, " ")
    assert podcast4.title is 'Untitled'
    assert podcast4.image is None


def test_podcast_change_title(my_podcast):
    my_podcast.title = "TourMix Podcast"
    assert my_podcast.title == "TourMix Podcast"

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_add_category(my_podcast):
    category = Category(12, "TV & Film")
    my_podcast.add_category(category)
    assert category in my_podcast.categories
    assert len(my_podcast.categories) == 1

    my_podcast.add_category(category)
    my_podcast.add_category(category)
    assert len(my_podcast.categories) == 1


def test_podcast_remove_category(my_podcast):
    category1 = Category(13, "Technology")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category1)
    assert len(my_podcast.categories) == 0

    category2 = Category(14, "Science")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category2)
    assert len(my_podcast.categories) == 1


def test_podcast_title_setter(my_podcast):
    my_podcast.title = "Dark Throne"
    assert my_podcast.title == 'Dark Throne'

    with pytest.raises(ValueError):
        my_podcast.title = " "

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_eq():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 == podcast1
    assert podcast1 != podcast2
    assert podcast2 != podcast3


def test_podcast_hash():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(100, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    podcast_set = {podcast1, podcast2, podcast3}
    assert len(podcast_set) == 2  # Since podcast1 and podcast2 have the same ID


def test_podcast_lt():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 < podcast2
    assert podcast2 > podcast3
    assert podcast3 > podcast1


def test_user_initialization():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert repr(user1) == "<User 1: shyamli>"
    assert repr(user2) == "<User 2: asma>"
    assert repr(user3) == "<User 3: jenny>"
    assert user2.password == "pw67890"
    with pytest.raises(ValueError):
        user4 = User(4, "xyz  ", "")
    with pytest.raises(ValueError):
        user4 = User(5, "    ", "qwerty12345")


def test_user_eq():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user4 = User(1, "Shyamli", "pw12345")
    assert user1 == user4
    assert user1 != user2
    assert user2 != user3


def test_user_hash():
    user1 = User(1, "   Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user_set = set()
    user_set.add(user1)
    user_set.add(user2)
    user_set.add(user3)
    assert sorted(user_set) == [user1, user2, user3]
    user_set.discard(user1)
    user_set.discard(user2)
    assert list(user_set) == [user3]


def test_user_lt():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert user1 < user2
    assert user2 < user3
    assert user3 > user1
    user_list = [user3, user2, user1]
    assert sorted(user_list) == [user1, user2, user3]


def test_user_add_remove_favourite_podcasts(my_user, my_subscription):
    my_user.add_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[<PodcastSubscription 1: Owned by shyamli>]"
    my_user.add_subscription(my_subscription)
    assert len(my_user.subscription_list) == 1
    my_user.remove_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[]"


def test_podcast_subscription_initialization(my_subscription):
    assert my_subscription.id == 1
    assert repr(my_subscription.owner) == "<User 1: shyamli>"
    assert repr(my_subscription.podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"

    assert repr(my_subscription) == "<PodcastSubscription 1: Owned by shyamli>"


def test_podcast_subscription_set_owner(my_subscription):
    new_user = User(2, "asma", "pw67890")
    my_subscription.owner = new_user
    assert my_subscription.owner == new_user

    with pytest.raises(TypeError):
        my_subscription.owner = "not a user"


def test_podcast_subscription_set_podcast(my_subscription):
    author2 = Author(2, "Author C")
    new_podcast = Podcast(200, author2, "Voices in AI")
    my_subscription.podcast = new_podcast
    assert my_subscription.podcast == new_podcast

    with pytest.raises(TypeError):
        my_subscription.podcast = "not a podcast"


def test_podcast_subscription_equality(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub3 = PodcastSubscription(2, my_user, my_podcast)
    assert sub1 == sub2
    assert sub1 != sub3


def test_podcast_subscription_hash(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub_set = {sub1, sub2}  # Should only contain one element since hash should be the same
    assert len(sub_set) == 1


def test_episode_initialisation():
    author1 = Author(2, "Venus")
    podcast1 = Podcast(1, author1, "Test1", "None", "Testing episode initialisation", "xyz.com", 5, "English")
    episode1 = Episode(1, podcast1, "Venus' first episode", "hello.com", "description", 5, "2017-12-27 00:50:29+00")
    assert repr(episode1) == "<Episode 1: 'Venus' first episode' in Podcast: Test1>"
    assert episode1.id == 1;
    assert episode1.title == "Venus' first episode"
    assert episode1.length == 5

    with pytest.raises(ValueError, match="Value must be a non-negative integer."):
        episode1 = Episode(1, podcast1, "Venus' first episode", "hello.com", "description", "hi", "2017-12-27 00:50:29+00")

    with pytest.raises(ValueError, match="Value must be a non-negative integer."):
        episode1 = Episode(-5, podcast1, "Venus' first episode", "hello.com", "description", 5, "2017-12-27 00:50:29+00")

    with pytest.raises(ValueError, match="Episode title must be a non-empty string."):
        episode1 = Episode(1, podcast1, 250, "hello.com", "description", 5, "2017-12-27 00:50:29+00")

    episode3 = Episode(3, podcast1, "Venus' first episode", "hello.com", "description", 5, "2017-12-27 00:50:29+00")
    assert episode3.id == 3
    episode3.title = "Ha - I have changed!"
    assert episode3.title == "Ha - I have changed!"


def test_episode_eq():
    author1 = Author(2, "Venus")
    podcast1 = Podcast(1, author1, "Test1", "None", "Testing episode equals", "xyz.com", 5, "English")
    episode1 = Episode(1, podcast1, "Venus' first episode", "hello.com", "description", 5, "2017-12-27 00:50:29+00")
    episode2 = Episode(1, podcast1, "Venus' first episode", "hello.com", "description", 5, "2017-12-27 00:50:29+00")
    episode3 = Episode(2, podcast1, "Venus' first episode", "hello.com", "description", 5, "2017-12-27 00:50:29+00")
    episode4 = Episode(2, podcast1, "Venus' first episode", "hello.com", "description", 5, "2017-12-27 00:50:29+00")
    episode9 = Episode(9, podcast1, "Venus' first episode", "hello.com", "description", 5, "2017-12-27 00:50:29+00")
    assert episode1 == episode2
    assert episode1 != episode3
    assert episode4 != episode9
    assert episode3 == episode4
    assert episode2 != episode9


def test_episode_lt():
    author1 = Author(1, "Michelle")
    author2 = Author(2, "Venus")
    podcast1 = Podcast(1, author1, "Test1", "None", "Testing episode less than", "xyz.com", 5, "English")
    podcast2 = Podcast(4, author2, "Test1", "None", "Testing episode initialisation", "xyz.com", 5, "English")
    episode1 = Episode(1, podcast1, "Venus' first episode", "hello.com", "description", 5, "2016-12-27 00:50:29+00")
    episode2 = Episode(1, podcast2, "Episode uno", "hello.com", "description", 5, "2017-12-27 00:48:29+00")
    episode3  =  Episode(1, podcast2, "Episode uno", "hello.com", "description", 5, "2021-12-27 00:50:27+00")
    episode9 = Episode(1, podcast1, "Venus' first episode", "hello.com", "description", 5, "2021-12-27 00:50:29+00")
    assert episode1 < episode2
    assert episode1 < episode3
    assert episode3 < episode9
    assert episode2 < episode3
    assert episode9 > episode1


def test_episode_hash():
    author1 = Author(1, "Michelle")
    author2 = Author(2, "Venus")
    podcast1 = Podcast(1, author1, "Test1", "None", "Testing episode less than", "xyz.com", 5, "English")
    podcast2 = Podcast(4, author2, "Test1", "None", "Testing episode initialisation", "xyz.com", 5, "English")
    episodes = set()
    episode1 = Episode(1, podcast2, "Episode uno", "hello.com", "description", 5, "2017-12-27 00:48:29+00")
    episode2 = Episode(2, podcast2, "Episode dos", "bye.com", "description-not", 2, "2007-03-24 00:22:29+00")
    episode3 = Episode(3, podcast1, "Episode tres", "something.com", "The number 3 is a very interesting number", 1, "2021-12-27 00:48:29+00")
    episodes.add(episode1)
    episodes.add(episode2)
    episodes.add(episode3)
    assert len(episodes) == 3
    episodes.discard(episode3)
    episodes.discard(episode2)
    assert len(episodes) == 1


def test_episode_title_setter():
    author1 = Author(1, "Andy")
    author2 = Author(2, "Venus")
    podcast1 = Podcast(1, author1, "TOY Story", "data:image/jpeg;base64,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", "The Toy story saga continues...", "https://www.pixar.com/feature-films/toy-story", 12, "English")
    episode1 = Episode(1, podcast1, "Andy the Cowboy", "toystory.com", "Toystory2", 9, "2015-01-12 00:22:29+00)")
    episode1.title = "Buzz the Buzzer"
    assert repr(episode1) == "<Episode 1: 'Buzz the Buzzer' in Podcast: TOY Story>"
    with pytest.raises(ValueError, match="Episode title must be a non-empty string."):
        episode1.title = 23


def test_episode_url_setter():
    author1 = Author(1, "Andy")
    podcast1 = Podcast(1, author1, "TOY Story",
                       "data:image/jpeg;base64,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",
                       "The Toy story saga continues...", "https://www.pixar.com/feature-films/toy-story", 12,
                       "English")
    episode1 = Episode(1, podcast1, "Andy the Cowboy", "toystory.com", "Toystory2", 9, "2015-01-12 00:22:29+00)")
    episode1.url = "https://www.disneyplus.com/en-nz"
    assert episode1.url == "https://www.disneyplus.com/en-nz"


def test_episode_description_setter():
    author1 = Author(1, "Andy")
    podcast1 = Podcast(1, author1, "TOY Story",
                       "data:image/jpeg;base64,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",
                       "The Toy story saga continues...", "https://www.pixar.com/feature-films/toy-story", 12,
                       "English")
    episode1 = Episode(1, podcast1, "Andy the Cowboy", "toystory.com", "Toystory2", 9, "2015-01-12 00:22:29+00)")
    episode1.description = "hello there"
    assert episode1.description == "hello there"


def test_episode_length_setter():
    author1 = Author(1, "Andy")
    podcast1 = Podcast(1, author1, "TOY Story",
                       "data:image/jpeg;base64,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",
                       "The Toy story saga continues...", "https://www.pixar.com/feature-films/toy-story", 12,
                       "English")
    episode1 = Episode(1, podcast1, "Andy the Cowboy", "toystory.com", "Toystory2", 9, "2015-01-12 00:22:29+00)")
    episode1.length = 2
    assert episode1.length == 2
    with  pytest.raises(ValueError, match="Value must be a non-negative integer."):
        episode1.length = "2"
    with pytest.raises(ValueError, match="Value must be a non-negative integer."):
        episode1.length = "5"


def test_episode_date_setter():
    author1 = Author(1, "Andy")
    podcast1 = Podcast(1, author1, "TOY Story",
                       "data:image/jpeg;base64,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",
                       "The Toy story saga continues...", "https://www.pixar.com/feature-films/toy-story", 12,
                       "English")
    episode1 = Episode(1, podcast1, "Andy the Cowboy", "toystory.com", "Toystory2", 9, "2015-01-12 00:22:29+00)")
    episode1.date = "2020-01-12 00:22:29+00"
    assert episode1.date == "2020-01-12 00:22:29+00"


# TODO : Write Unit Tests for Review class


# TODO: Write Unit Tests for Playlist class
