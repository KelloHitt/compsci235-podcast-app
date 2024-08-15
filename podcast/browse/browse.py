from flask import Blueprint, render_template
import podcast.adapters.repository as repository
import podcast.browse.services as services

browse_blueprint = Blueprint('browse_bp', __name__)


@browse_blueprint.route('/browse/<int:page_number>', methods=['GET'])
def show_podcasts(page_number):
    pagination_data = services.get_podcasts_by_page(repository.repo_instance, page_number)
    return render_template('catalogue.html', **pagination_data)  # Unpack the dictionary
