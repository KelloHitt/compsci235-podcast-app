from sqlalchemy import inspect
from podcast.adapters.orm import mapper_registry


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors', 'categories', 'episodes', 'playlist_episodes', 'playlists',
                                           'podcast_categories', 'podcasts', 'reviews', 'users']

# TODO: more testing cases
