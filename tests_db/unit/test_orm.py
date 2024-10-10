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
    empty_session.execute('INSERT INTO podcasts (title, image_url, description, language, website_url, author_id, itunes_id) VALUES'
                          '("D-Hour Radio Network",'
                          '"http://is3.mzstatic.com/image/thumb/Music118/v4/b9/ed/86/b9ed8603-d94b-28c5-5f95-8b7061bf22fa/source/600x600bb.jpg", '
                          '"The D-Hour Radio Network is the home of real entertainment radio and ""THE"" premiere online radio network. We showcase dynamically dynamite radio shows for the sole purpose of entertaining your listening ear. Here on the D-hour Show Radio network we take pride in providing an outlet for Celebrity Artists, Underground Artists, Indie Artists, Producers, Entertainers, Entrepreneurs, Internet Stars and future business owners. We discuss topics of all forms and have a great time while doing so. We play all your favorite hits in the forms of Celebrity, Indie, Hip Hop, Soul/R&B, Pop, and everything else you want and consider popular. If you would like yourself and or your music to be showcased on our radio network submit email requests for music airplay, interviews and etc.. to:  dhourshow@gmail.com and we will get back to you promptly. Here at the D-Hour Radio Network we are Family and all of our guests, listeners and loyal fans are family too.  So tune into the D-Hour Radio Network and join the Family! ", '
                          '"English", '
                          '"http://www.blogtalkradio.com/dhourshow", '
                          '1, '
                          '538283940,')
    row = empty_session.execute('SELECT id from podcasts').fetchone()
    return row[0]

def make_podcast():
    author = make_author()
    podcast = Podcast(1, author, "Podcast 1", "image", "Description 1", "Website 1", 1234, "English")
    return podcast

def insert_episode(empty_session):
    empty_session.execute(text('INSERT INTO episodes (episode_id, podcast_id, title, audio_url, description, pub_date) '
                               'VALUES (1) (1) ("Podcast 1") ("Audio URL 1") ("A podcast") ("8/10/2024")'))
    rows = list(empty_session.execute(text('SELECT episode_id from episodes')))
    keys = tuple(row[0] for row in rows)
    return keys

def make_episode():
    podcast = make_podcast()
    episode = Episode(1, podcast, "Title", "Website", "Description", 123, "8/10/2024")

def insert_author(empty_session):
    empty_session.execute(text('INSERT INTO authors (author_id, name) VALUES (1) ("Author 1")'))
    rows = list(empty_session.execute(text('SELECT author_id from authors')))
    keys = tuple(row[0] for row in rows)
    return keys

def make_author():
    author = Author(1, "Author 1")
    return author

def insert_review(empty_session):
    empty_session.execute(text('INSERT INTO reviews (user_id, podcast_id, rating, comment) VALUES (1) (1) (5) ("Good")'))
    rows = list(empty_session.execute(text('SELECT review_id from reviews')))
    keys = tuple(row[0] for row in rows)
    return keys

def make_review():
    podcast = make_podcast()
    reviewer = make_user()
    review = Review(1, podcast, reviewer, 1, "Review Text")
    return review

def insert_categories(empty_session):
    empty_session.execute('INSERT INTO categories (category_name) VALUES ("Sports") ("News")')
    rows = list(empty_session.execute(text('SELECT id from categories')))
    keys = tuple(row[0] for row in rows)
    return keys

def make_category():
    category = Category(1, "Sport")
    return category

def insert_podcast_category_associations(empty_session, podcast_key, category_keys):
    pass

def insert_playlist_episode_associations(empty_session, playlist_key, episode_keys):
    pass

def insert_reviewed_podcast(empty_session):
    pass

def test_loading_of_podcast(empty_session):
    pass

def test_loading_of_categorised_podcast(empty_session):
    pass

def test_loading_of_reviewed_podcast(empty_session):
    pass

def test_saving_of_review(empty_session):
    pass

def test_saving_of_podcast(empty_session):
    pass

def test_saving_of_categorised_podcast(empty_session):
    pass

def test_save_reviewed_podcast(empty_session):
    pass

