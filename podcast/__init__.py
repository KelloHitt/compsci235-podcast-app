"""Initialize Flask app."""
from pathlib import Path
from flask import Flask, render_template
import podcast.adapters.repository as repo
from podcast.adapters.memory_repository import MemoryRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    # Fill the content with the repository from the provided csv files
    data_path = Path("./podcast/adapters/data")
    csv_data_reader = CSVDataReader()
    csv_data_reader.populate_data(data_path, repo.repo_instance)

    with app.app_context():
        # Register blueprints
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .description import description
        app.register_blueprint(description.description_blueprint)

        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)

    return app
