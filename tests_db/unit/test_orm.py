from podcast.domainmodel.model import User, Podcast, Episode, Author, Review, Category
from sqlalchemy.sql import text
import pytest
from sqlalchemy.exc import IntegrityError

def insert_user(empty_session, values=None):
    new_username = "John"
    new_password = "Passw0rd"

    if values is not None:
        new_username = values[0]
        new_password = values[1]

    empty_session.execute(text('INSERT INTO users (user_name, password) VALUES (:user_name, :password)'),
                          {'user_name': new_username, 'password': new_password})

    row = empty_session.execute(text('SELECT user_id from users where user_name = :user_name'),
                                {'user_name': new_username}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute(text('INSERT INTO users (user_name, password) VALUES (:user_name, :password)'),
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute(text('SELECT user_id from users')))
    keys = tuple(row[0] for row in rows)
    return keys

def make_user():
    user = User(1, "John", "Passw0rd")
    return user

def test_loading_of_users(empty_session):
    users = list()
    users.append((1, "John", "Passw0rd"))
    users.append((2, "Dan", "123456Ab"))
    insert_users(empty_session, users)

    expected = [
        User(1, "John", "Passw0rd"),
        User(2, "Dan", "123456Ab")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT user_name, password FROM users')))
    assert rows == [("John", "Passw0rd")]

def test_saving_of_users_with_common_username(empty_session):
    insert_user(empty_session, (1, "John", "Passw0rd"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User(1, "John", "123456Ab")
        empty_session.add(user)
        empty_session.commit()

def insert_podcast(empty_session):
    author_id = insert_author(empty_session)
    empty_session.execute(text('INSERT INTO podcasts (podcast_id, title, image_url, description, language, website_url, author_id, itunes_id) VALUES '
                               '(:podcast_id, :title, :image_url, :description, :language, :website_url, :author_id, :itunes_id)'),
                          {'podcast_id': 1, 'title': "D-Hour Radio Network",
                           'image_url': "http://is3.mzstatic.com/image/thumb/Music118/v4/b9/ed/86/b9ed8603-d94b-28c5-5f95-8b7061bf22fa/source/600x600bb.jpg",
                           'description': "The D-Hour Radio Network is the home of real entertainment radio and ""THE"" premiere online radio network. We showcase dynamically dynamite radio shows for the sole purpose of entertaining your listening ear. Here on the D-hour Show Radio network we take pride in providing an outlet for Celebrity Artists, Underground Artists, Indie Artists, Producers, Entertainers, Entrepreneurs, Internet Stars and future business owners. We discuss topics of all forms and have a great time while doing so. We play all your favorite hits in the forms of Celebrity, Indie, Hip Hop, Soul/R&B, Pop, and everything else you want and consider popular. If you would like yourself and or your music to be showcased on our radio network submit email requests for music airplay, interviews and etc.. to:  dhourshow@gmail.com and we will get back to you promptly. Here at the D-Hour Radio Network we are Family and all of our guests, listeners and loyal fans are family too.  So tune into the D-Hour Radio Network and join the Family! ",
                           'language': "English",
                           'website_url': "http://www.blogtalkradio.com/dhourshow",
                           'author_id': author_id,
                           'itunes_id': 538283940})
    row = empty_session.execute(text('SELECT podcast_id from podcasts')).fetchone()
    return row[0]

def make_podcast():
    author = make_author()
    podcast = Podcast(1, author, "Podcast 1", "image", "Description 1", "Website 1", 1234, "English")
    return podcast

def insert_episode(empty_session):
    empty_session.execute(text('INSERT INTO episodes (episode_id, podcast_id, title, audio_url, description, pub_date) '
                               'VALUES (:episode_id, :podcast_id, :title, :audio_url, :description, :pub_date)'),
                          {'episode_id': 1, 'podcast_id': 1, 'title': "Podcast 1", 'audio_url': "Audio URL 1", 'description': "Description 1", 'pub_date': "8/10/2024"})
    rows = list(empty_session.execute(text('SELECT episode_id from episodes')))
    keys = tuple(row[0] for row in rows)
    return keys[0]

def make_episode():
    podcast = make_podcast()
    episode = Episode(1, podcast, "Title", "Website", "Description", 123, "8/10/2024")
    return episode

def insert_author(empty_session):
    empty_session.execute(text('INSERT INTO authors (author_id, name) VALUES (:author_id, :name)'),
                          {'author_id': 1, 'name': "Author 1"})
    rows = list(empty_session.execute(text('SELECT author_id from authors')))
    keys = tuple(row[0] for row in rows)
    return keys[0]

def make_author():
    author = Author(1, "Author 1")
    return author

def insert_review(empty_session):
    empty_session.execute(text('INSERT INTO reviews (user_id, podcast_id, rating, comment) VALUES (:user_id, :podcast_id, :rating, :comment)'),
                          {'user_id': 1, 'podcast_id': 1, 'rating': 5, 'comment': "Good Podcast"})
    rows = list(empty_session.execute(text('SELECT review_id from reviews')))
    keys = tuple(row[0] for row in rows)
    return keys

def make_review():
    podcast = make_podcast()
    reviewer = make_user()
    review = Review(1, podcast, reviewer, 1, "Review Text")
    return review

def insert_categories(empty_session):
    empty_session.execute(text('INSERT INTO categories (category_name) VALUES (:category_name)'),
                          {'category_name': "Sports"})
    empty_session.execute(text('INSERT INTO categories (category_name) VALUES (:category_name)'),
                          {'category_name': "News"})
    rows = list(empty_session.execute(text('SELECT category_id from categories')))
    keys = tuple(row[0] for row in rows)
    return keys

def make_category():
    category = Category(1, "Sport")
    return category

def insert_podcast_category_associations(empty_session, podcast_key, category_keys):
    stmt = text('INSERT INTO podcast_categories (podcast_id, category_id) VALUES (:podcast_id, :category_id)')
    for category_key in category_keys:
        empty_session.execute(stmt, {'podcast_id': podcast_key, 'category_id': category_key})

def insert_playlist_episode_associations(empty_session, playlist_key, episode_keys):
    stmt = text('INSERT INTO playlist_episodes (playlist_id, episode_id) VALUES (:playlist_id, :episode_id)')
    for episode_key in episode_keys:
        empty_session.execute(stmt, {'playlist_id': playlist_key, 'episode_id': episode_key})

def insert_reviewed_podcast(empty_session):
    podcast_key = insert_podcast(empty_session)
    user_key = insert_user(empty_session)
    empty_session.execute(text('INSERT INTO reviews (user_id, podcast_id, rating, comment) VALUES'
        '(:user_id, :podcast_id, :rating, :comment)'),
        {'user_id': user_key, 'podcast_id': podcast_key, 'rating': 3, 'comment': "Review Comment"})
    row = empty_session.execute(text('SELECT podcast_id from podcasts')).fetchone()
    return row[0]

def test_loading_of_podcast(empty_session):
    podcast_key = insert_podcast(empty_session)
    expected_podcast = make_podcast()
    fetched_podcast = empty_session.query(Podcast).one()
    assert expected_podcast == fetched_podcast
    assert podcast_key == fetched_podcast.id

def test_loading_of_categorised_podcast(empty_session):
    podcast_key = insert_podcast(empty_session)
    category_keys = insert_categories(empty_session)
    insert_podcast_category_associations(empty_session, podcast_key, category_keys)
    podcast = empty_session.get(Podcast, podcast_key)
    categories = [empty_session.get(Category, key) for key in category_keys]
    for category in categories:
        assert category in podcast.categories

def test_loading_of_reviewed_podcast(empty_session):
    podcast_key = insert_reviewed_podcast(empty_session)
    podcast = empty_session.get(Podcast, podcast_key)
    reviews = podcast.reviews
    assert len(reviews) > 0
    assert reviews[0].content == "Review Comment"

def test_saving_of_review(empty_session):
    review = make_review()
    empty_session.add(review)
    empty_session.commit()
    rows = list(empty_session.execute(text('SELECT user_id, podcast_id, comment FROM reviews')))
    assert rows == [(1, 1, "Review Text")]

def test_saving_of_podcast(empty_session):
    podcast = make_podcast()
    empty_session.add(podcast)
    empty_session.commit()
    rows = list(empty_session.execute(text('SELECT title, image_url, description, language, website_url FROM podcasts')))
    assert rows == [("Podcast 1", "image", "Description 1", "English", "Website 1")]

def test_saving_of_episode(empty_session):
    episode = make_episode()
    empty_session.add(episode)
    empty_session.commit()
    rows = list(empty_session.execute(text('SELECT episode_id, podcast_id, title, audio_url, description, pub_date FROM episodes')))
    assert rows == [(1, 1, "Title", "Website", "Description", "8/10/2024")]

def test_loading_of_episode(empty_session):
    episode_key = insert_episode(empty_session)
    expected_episode = make_episode()
    fetched_episode = empty_session.query(Episode).one()
    assert expected_episode == fetched_episode
    assert episode_key == fetched_episode.id

def test_multiple_episodes_in_podcast(empty_session):
    podcast_key = insert_podcast(empty_session)
    insert_episode(empty_session)
    empty_session.execute(text('INSERT INTO episodes (episode_id, podcast_id, title, audio_url, description, pub_date) VALUES '
                               '(:episode_id, :podcast_id, :title, :audio_url, :description, :pub_date)'),
                               {'episode_id': 2, 'podcast_id': podcast_key, 'title': "Title 2", 'audio_url': "Audio URL 2", 'description': "Description 2", 'pub_date': "12/12/2024"})
    episodes = empty_session.query(Episode).filter_by(podcast_id=podcast_key).all()
    assert len(episodes) == 2
    assert episodes[0]._title == "Podcast 1"
    assert episodes[1]._title == "Title 2"

def test_add_episode_to_playlist(empty_session):
    user_key = insert_user(empty_session)
    empty_session.execute(text('INSERT INTO playlists (name, owner_id) VALUES ("My Playlist", :owner_id)'),
                                              {'owner_id': user_key})
    playlist_key = empty_session.execute(text('SELECT playlist_id FROM playlists WHERE name = "My Playlist"')).fetchone()[0]
    episode_key = insert_episode(empty_session)
    empty_session.execute(text('INSERT INTO playlist_episodes (playlist_id, episode_id) VALUES (:playlist_id, :episode_id)'),
                               {'playlist_id': playlist_key, 'episode_id': episode_key})
    rows = list(empty_session.execute(text('SELECT episode_id FROM playlist_episodes WHERE playlist_id = :playlist_id'),
                                           {'playlist_id': playlist_key}))
    assert rows[0][0] == episode_key

def test_delete_review(empty_session):
    review_key = insert_review(empty_session)
    review = empty_session.get(Review, review_key)
    assert review_key is not None
    empty_session.delete(review)
    empty_session.commit()
    deleted_review = empty_session.get(Review, review_key)
    assert deleted_review is None

def test_delete_episode_from_playlist(empty_session):
    user_key = insert_user(empty_session)
    empty_session.execute(text('INSERT INTO playlists (name, owner_id) VALUES ("My Playlist", :owner_id)'),
                          {'owner_id': user_key})
    playlist_key = empty_session.execute(text('SELECT playlist_id FROM playlists WHERE name = "My Playlist"')).fetchone()[0]
    episode_key = insert_episode(empty_session)
    empty_session.execute(text('INSERT INTO playlist_episodes (playlist_id, episode_id) VALUES (:playlist_id, :episode_id)'),
                          {'playlist_id': playlist_key, 'episode_id': episode_key})
    rows = list(empty_session.execute(text('SELECT episode_id FROM playlist_episodes WHERE playlist_id = :playlist_id'),
                                      {'playlist_id': playlist_key}))
    assert rows[0][0] == episode_key
    empty_session.execute(text('DELETE FROM playlist_episodes WHERE playlist_id = :playlist_id AND episode_id = :episode_id'),
                          {'playlist_id': playlist_key, 'episode_id': episode_key})
    empty_session.commit()
    rows_without_episode = list(empty_session.execute(text('SELECT episode_id FROM playlist_episodes WHERE playlist_id = :playlist_id'),
                                                      {'playlist_id': playlist_key}))
    assert len(rows_without_episode) == 0

def test_loading_of_author(empty_session):
    author = make_author()
    empty_session.add(author)
    empty_session.commit()
    rows = list(empty_session.execute(text('SELECT author_id, name FROM authors')))
    assert rows == [(1, "Author 1")]

def test_saving_of_author(empty_session):
    author_key = insert_author(empty_session)
    expected_author = make_author()
    fetched_author = empty_session.query(Author).one()
    assert expected_author == fetched_author
    assert author_key == fetched_author.id
