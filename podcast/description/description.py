from flask import Blueprint, render_template

import podcast.adapters.repository as repository
import podcast.description.services as services
import podcast.utilities.utilities as utilities

description_blueprint = Blueprint(
    'description_bp', __name__)


@description_blueprint.route('/description/<int:podcast_id>', methods=['GET'])
def show_description(podcast_id):
    podcast = services.get_podcast_by_id(repository.repo_instance, podcast_id)
    episodes = sorted(podcast.episodes, key=lambda episode: episode.date)
    categories = utilities.get_categories()['categories']
    return render_template('podcastDescription.html', podcast=podcast, episodes=episodes, categories=categories)
