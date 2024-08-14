"""Initialize Flask app."""
from pathlib import Path
from flask import Flask, render_template
import podcast.adapters.repository as repo
from podcast.adapters.memory_repository import MemoryRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader

# TODO: Access to the podcast should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
from podcast.domainmodel.model import Podcast, Author


# TODO: Access to the podcast should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
def create_some_podcast():
    some_author = Author(1, "TED")
    some_podcast = Podcast(66, some_author, "TED Talks Daily")
    some_podcast.description = "Want TED Talks on the go? Every weekday, this feed brings you our latest talks in audio format. Hear thought-provoking ideas on every subject imaginable -- from Artificial Intelligence to Zoology, and everything in between -- given by the world's leading thinkers and doers. This collection of talks, given at TED and TEDx conferences around the globe, is also available in video format."
    some_podcast.image_url = "http://is4.mzstatic.com/image/thumb/Music128/v4/d5/c6/50/d5c65035-505e-b006-48e5-be3f0f8f19f8/source/600x600bb.jpg"
    return some_podcast


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('podcast') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    # fill the content of the repository from the provided csv files
    csv_data_reader = CSVDataReader()
    csv_data_reader.populate_data(data_path, repo.repo_instance)

    @app.route('/')
    def home():
        some_podcast = create_some_podcast()
        # Use Jinja to customize a predefined html page rendering the layout for showing a single podcast.
        return render_template('podcastDescription.html', podcast=some_podcast)

    return app
