from flask import Blueprint, render_template
import podcast.adapters.repository as repository
import podcast.browse.services as services
import podcast.utilities.utilities as utilities

browse_blueprint = Blueprint('browse_bp', __name__)


@browse_blueprint.route('/browse/<int:page_number>', methods=['GET'])
@browse_blueprint.route('/browse/category/<string:category>/<int:page_number>', methods=['GET'])
def show_podcasts(page_number, category=None):
    if category:
        pagination_data = services.get_podcasts_by_category(repository.repo_instance, category, page_number)
    else:
        pagination_data = services.get_podcasts_by_page(repository.repo_instance, page_number)

    return render_template('catalogue.html', **pagination_data)


# Register a template context processor function which runs before rendering the template
@browse_blueprint.context_processor
def inject_categories():
    return utilities.get_categories()
