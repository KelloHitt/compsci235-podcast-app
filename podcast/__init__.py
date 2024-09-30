"""Initialize Flask app."""
import os
from pathlib import Path

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import podcast.adapters.repository as repo
from podcast.adapters import database_repository
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.memory_repository import MemoryRepository
from podcast.adapters.orm import metadata, map_model_to_tables
from podcast.adapters.repository_populate import populate_data


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "adapters/data"))

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == "memory":
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = MemoryRepository()
        # Fill the content with the repository from the provided csv files
        populate_data(repo.repo_instance, data_path)

    elif app.config['REPOSITORY'] == "database":
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(
            database_uri,
            connect_args={"check_same_thread": False},
            poolclass=NullPool,
            echo=database_echo,
        )
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        if app.config["TESTING"] == "True" or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            database_mode = True
            populate_data(repo.repo_instance, data_path)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            map_model_to_tables()

    with app.app_context():
        # Register blueprints
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .description import description
        app.register_blueprint(description.description_blueprint)

        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .user import user
        app.register_blueprint(user.user_blueprint)

        from .search import search
        app.register_blueprint(search.search_blueprint)

    return app
