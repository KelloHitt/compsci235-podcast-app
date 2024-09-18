from flask import Blueprint, render_template, request

import podcast.adapters.repository as repository
import podcast.browse.services as services
import podcast.utilities.utilities as utilities

browse_blueprint = Blueprint('browse_bp', __name__)


@browse_blueprint.route('/browse', methods=['GET'])
def show_podcasts():
    # Extract query parameters for page number and category
    page_number = request.args.get('page_number', default=1, type=int)
    category = request.args.get('category', default=None, type=str)

    # Ensure page_number is within valid range
    if page_number > 100:
        page_number = 100
    if page_number < 1:
        page_number = 1

    # Retrieve podcasts by category if specified, otherwise by page
    if category:
        pagination_data = services.get_podcasts_by_category(repository.repo_instance, category, page_number)
    else:
        pagination_data = services.get_podcasts_by_page(repository.repo_instance, page_number)

    # Render the catalogue page with the retrieved data
    return render_template('description/catalogue.html', **pagination_data)


# Register a template context processor function which runs before rendering the template
@browse_blueprint.context_processor
def inject_categories():
    return utilities.get_categories()
