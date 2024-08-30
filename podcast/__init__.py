"""Initialize Flask app."""
import os
from pathlib import Path

from flask import Flask

import podcast.adapters.repository as repo
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.memory_repository import MemoryRepository, populate_data


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

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    # Fill the content with the repository from the provided csv files
    populate_data(repo.repo_instance, data_path)

    with app.app_context():
        # Register blueprints
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .description import description
        app.register_blueprint(description.description_blueprint)

        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)

    return app
