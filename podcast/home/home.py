from flask import Blueprint, render_template
import podcast.adapters.repository as repository
import podcast.home.services as services

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    list_of_podcasts = services.get_random_podcasts_info(repository.repo_instance)
    return render_template('layout.html', list_of_podcasts=list_of_podcasts)
