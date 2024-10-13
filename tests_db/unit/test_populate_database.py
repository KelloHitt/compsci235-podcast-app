from sqlalchemy import inspect, select
from podcast.adapters.orm import mapper_registry


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors', 'categories', 'episodes', 'playlist_episodes', 'playlists',
                                           'podcast_categories', 'podcasts', 'reviews', 'users']


def test_database_populate_select_all_authors(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_authors_table = inspector.get_table_names()[0]
    print("name_of_authors_table", name_of_authors_table)

    with database_engine.connect() as connection:
        # query for records in table authors
        select_statement = select(mapper_registry.metadata.tables[name_of_authors_table])
        result = connection.execute(select_statement)

    author_names = []
    for row in result:
        author_names.append(row[1])

    assert len(author_names) == 3
    assert author_names[0] == 'D Hour Radio Network'
    assert author_names[1] == 'Brian Denny'
    assert author_names[2] == 'Tallin Country Church'


def test_database_populate_select_all_categories(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_categories_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table category
        select_statement = select(mapper_registry.metadata.tables[name_of_categories_table])
        result = connection.execute(select_statement)

        category_names = []
        for row in result:
            category_names.append(row[1])

        assert len(category_names) == 3
        assert category_names[0] == 'Society & Culture'
        assert category_names[1] == 'Professional'
        assert category_names[2] == 'Comedy'


def test_database_populate_select_all_episodes(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_episodes_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table episodes
        select_statement = select(mapper_registry.metadata.tables[name_of_episodes_table])
        result = connection.execute(select_statement)

        all_episodes = []
        for row in result:
            all_episodes.append((row[1], row[2], row[4], row[5]))

        assert len(all_episodes) == 4
        assert all_episodes[0] == (None, 'Choir', 'Choir', '2017-12-01 10:03:18')
        assert all_episodes[1] == (2, '#05: Comixology, Runaways, and Star Trek',
                                   "We're back for a spiritually exhausting episode of the Meandercast! We cover "
                                   "Comixology, Hulu's Marvel's Runaways, and Star Trek: Discovery. This one got a "
                                   "little away from us this time. Forthcoming episodes will probably not be this "
                                   "long.",
                                   '2017-12-01 13:00:05')
        assert all_episodes[-1] == (3, 'Caller Of The Week Part 1.', 'The best of Greg & The Morning Buzz. Listen '
                                                                     'weekdays 5:30am to 10am.',
                                    '2017-12-01 14:29:35')


def test_database_populate_select_all_playlist_episodes(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_playlist_episodes_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table playlist_episodes
        select_statement = select(mapper_registry.metadata.tables[name_of_playlist_episodes_table])
        result = connection.execute(select_statement)

    all_playlist_episodes = []
    for row in result:
        all_playlist_episodes.append((row[1], row[2]))

    assert len(all_playlist_episodes) == 0


def test_database_populate_select_all_playlists(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_playlist_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table playlists
        select_statement = select(mapper_registry.metadata.tables[name_of_playlist_table])
        result = connection.execute(select_statement)

    all_playlists = []
    for row in result:
        all_playlists.append((row[1], row[2]))

    assert len(all_playlists) == 0


def test_database_populate_select_all_podcast_categories(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_podcasts_categories_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table podcast_categories
        select_statement = select(mapper_registry.metadata.tables[name_of_podcasts_categories_table])
        result = connection.execute(select_statement)

    all_podcast_categories = []
    for row in result:
        all_podcast_categories.append((row[1], row[2]))

    assert len(all_podcast_categories) == 6
    assert all_podcast_categories[0] == (1, 1)
    assert all_podcast_categories[2] == (2, 2)
    assert all_podcast_categories[4] == (3, 1)
    assert all_podcast_categories[5] == (4, 3)


def test_database_populate_select_all_podcasts(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_podcasts_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # query for records in table podcasts
        select_statement = select(mapper_registry.metadata.tables[name_of_podcasts_table])
        result = connection.execute(select_statement)

        all_podcasts = []
        for row in result:
            all_podcasts.append((row[0], row[1], row[2], row[3],
                                 row[4], row[5], row[6], row[7]))

        assert len(all_podcasts) == 4
        assert all_podcasts[0] == (1, 'D-Hour Radio Network',
                                   'http://is3.mzstatic.com/image/thumb/Music118/v4/b9/ed/86/b9ed8603-d94b-28c5-5f95'
                                   '-8b7061bf22fa/source/600x600bb.jpg',
                                   'The D-Hour Radio Network is the home of real entertainment radio and the premiere '
                                   'online radio network.',
                                   'English', 'http://www.blogtalkradio.com/dhourshow', 1, 538283940)
        assert all_podcasts[1] == (2, 'Brian Denny Radio',
                                   'http://is5.mzstatic.com/image/thumb/Music111/v4/49/c8/19/49c8190a-ca0f-f32c-c089'
                                   '-d7ae502d2cb8/source/600x600bb.jpg',
                                   '5-in-1: Brian Denny Radio is the fastest podcast in all the land.', 'English',
                                   'http://thebdshow.libsyn.com/podcast', 2, 1132261215)
        assert all_podcasts[-1] == (4, 'Tallin Messages',
                                    'http://is3.mzstatic.com/image/thumb/Music71/v4/d6/7a/a2/d67aa202-4c97-70d3-e629'
                                    '-b830567cff78/source/600x600bb.jpg',
                                    'Podcast by Tallin Country Church', 'English',
                                    'http://soundcloud.com/tallin-church', 3, 1165994461)


def test_database_populate_select_all_reviews(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        # query for records in table reviews
        select_statement = select(mapper_registry.metadata.tables[name_of_reviews_table])
        result = connection.execute(select_statement)

    all_reviews = []
    for row in result:
        all_reviews.append((row[0], row[1], row[2], row[3]))

    assert len(all_reviews) == 0


def test_database_populate_select_all_users(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[8]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select(mapper_registry.metadata.tables[name_of_users_table])
        result = connection.execute(select_statement)

    all_users = []
    for row in result:
        all_users.append((row[0], row[1]))

    assert len(all_users) == 0
