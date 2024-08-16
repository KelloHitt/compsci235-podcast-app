from flask import Blueprint, render_template
import podcast.adapters.repository as repository
import podcast.home.services as services
import podcast.utilities.utilities as utilities

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    list_of_podcasts = services.get_random_podcasts_info(repository.repo_instance)
    categories = utilities.get_categories()['categories']
    return render_template('index.html', list_of_podcasts=list_of_podcasts, categories=categories)
