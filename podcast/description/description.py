from flask import Blueprint, render_template
import podcast.adapters.repository as repository
import podcast.description.services as services

description_blueprint = Blueprint(
    'description_bp', __name__)


@description_blueprint.route('/description/<int:podcast_id>', methods=['GET'])
def show_description(podcast_id):
    podcast = services.get_podcast_by_id(repository.repo_instance, podcast_id)
    return render_template('podcastDescription.html', podcast=podcast)
