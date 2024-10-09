from sqlalchemy import (
    Table, Column, Integer, Float, String, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import registry, relationship
from datetime import datetime, date

from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode, Playlist

# Global variable giving access to the MetaData (schema) information of the database
mapper_registry = registry()

authors_table = Table(
    'authors', mapper_registry.metadata,
    Column('author_id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True)
)

podcast_table = Table(
    'podcasts', mapper_registry.metadata,
    Column('podcast_id', Integer, primary_key=True),
    Column('title', Text, nullable=True),
    Column('image_url', Text, nullable=True),
    Column('description', String(255), nullable=True),
    Column('language', String(255), nullable=True),
    Column('website_url', String(255), nullable=True),
    Column('author_id', ForeignKey('authors.author_id')),
    Column('itunes_id', Integer, nullable=True)
)

# Episodes should have links to its podcast through its foreign keys
episode_table = Table(
    'episodes', mapper_registry.metadata,
    Column('episode_id', Integer, primary_key=True),
    Column('podcast_id', Integer, ForeignKey('podcasts.podcast_id')),
    Column('title', Text, nullable=True),
    Column('audio_url', Text, nullable=True),
    Column('description', String(255), nullable=True),
    Column('pub_date', Text, nullable=True)
)

categories_table = Table(
    'categories', mapper_registry.metadata,
    Column('category_id', Integer, primary_key=True, autoincrement=True),
    Column('category_name', String(64))  # , nullable=False)
)

# TODO : Association table podcast_categories
# Resolve many-to-many relationship between podcast and categories
podcasts_categories_table = Table(
    'podcast_categories', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('category_id', ForeignKey('categories.category_id')) #Do we need to show podcast name and category name as well??
)

# TODO : Table users_table
# Resolve definition for User table and the necessary code that maps the table to its domain model class
users_table = Table(
    'users', mapper_registry.metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(225), nullable=True),
    Column('password', String(225), nullable=True)
)

# TODO : Table reviews_table
# Resolve definition for Review table and the necessary code that maps the table to its domain model class
# Reviews should have links to its podcast and user through its foreign keys
reviews_table = Table(
    'reviews', mapper_registry.metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('podcast_id', ForeignKey('podcasts.podcast_id'), primary_key=True),
    Column('rating', Integer, nullable=False),
    Column('comment', String(225), nullable=True),
)

playlists_table = Table(
    'playlists', mapper_registry.metadata,
    Column('playlist_id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(225), nullable=True),
    Column('owner', ForeignKey('users.user_id'), nullable=True)
)

# Resolve many-to-many relationship between playlists and episodes
playlists_episodes_table = Table(
 'playlist_episodes', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('playlist_id', ForeignKey('playlists.playlist_id')),
    Column('episode_id', ForeignKey('episodes.episode_id')),
)

def map_model_to_tables():
    mapper_registry.map_imperatively(Author, authors_table, properties={
        '_id': authors_table.c.author_id,
        '_name': authors_table.c.name,
    })

    mapper_registry.map_imperatively(Category, categories_table, properties={
        '_id': categories_table.c.category_id,
        '_name': categories_table.c.category_name,
    })

    mapper_registry.map_imperatively(Podcast, podcast_table, properties={
        '_id': podcast_table.c.podcast_id,
        '_title': podcast_table.c.title,
        '_image': podcast_table.c.image_url,
        '_description': podcast_table.c.description,
        '_language': podcast_table.c.language,
        '_website': podcast_table.c.website_url,
        '_itunes_id': podcast_table.c.itunes_id,
        '_author': relationship(Author),
        'episodes': relationship(Episode, back_populates='_podcast'),
        'categories': relationship(Category, secondary=podcasts_categories_table),
        'reviews': relationship(Review, back_populates='_podcast')
    })

    mapper_registry.map_imperatively(Episode, episode_table, properties={
        '_id': episode_table.c.episode_id,
        '_podcast': relationship(Podcast, back_populates='episodes'),
        '_title': episode_table.c.title,
        '_url': episode_table.c.audio_url,
        '_description': episode_table.c.description,
        '_date': episode_table.c.pub_date,
    })

    mapper_registry.map_imperatively(User, users_table, properties={
        '_id': users_table.c.user_id,
        '_username': users_table.c.user_name,
        '_password': users_table.c.password,
        '_reviews': relationship(Review, back_populates='_reviewer'),
        '_playlist': relationship(Playlist, back_populates='_owner')

    })

    mapper_registry.map_imperatively(Review, reviews_table, properties={
        '_reviewer': relationship(User, back_populates='_reviews'),
        '_podcast': relationship(Podcast, back_populates='reviews'),
        '_rating': reviews_table.c.rating,
        '_content': reviews_table.c.comment,
    })

    mapper_registry.map_imperatively(Playlist, playlists_table, properties={
        '_id': playlists_table.c.playlist_id,
        '_name': playlists_table.c.name,
        '_owner': relationship(User, back_populates='_playlist'),
        '_episodes': relationship(Episode, secondary=playlists_episodes_table)
    })
