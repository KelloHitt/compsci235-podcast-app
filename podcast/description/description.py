from flask import Blueprint, render_template, request

import podcast.adapters.repository as repository
import podcast.description.services as services
import podcast.utilities.utilities as utilities

description_blueprint = Blueprint('description_bp', __name__)


@description_blueprint.route('/description', methods=['GET'])
def show_description():
    podcast_id = request.args.get('podcast_id', default=1, type=int)

    # Ensure podcast_id is within valid range
    if podcast_id > 1000:
        podcast_id = 1000
    if podcast_id < 1:
        podcast_id = 1

    podcast = services.get_podcast_by_id(repository.repo_instance, podcast_id)
    episodes = sorted(podcast.episodes, key=lambda episode: episode.date)
    categories = utilities.get_categories()['categories']

    return render_template('podcastDescription.html', podcast=podcast, episodes=episodes, categories=categories)
