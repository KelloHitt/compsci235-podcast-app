"""Initialize Flask app."""
import os
from pathlib import Path
from flask import Flask, render_template
import podcast.adapters.repository as repo
from podcast.adapters.memory_repository import MemoryRepository, populate_data
from podcast.adapters.datareader.csvdatareader import CSVDataReader


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    # Fill the content with the repository from the provided csv files
    data_path = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "adapters/data"))
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
