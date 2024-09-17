
from flask import Blueprint, render_template, request
import podcast.adapters.repository as repository
import podcast.search.services as services
import math

search_blueprint = Blueprint(
    'search_bp', __name__)


@search_blueprint.route('/search', methods=['GET'])
def search():
    return render_template('search.html')


@search_blueprint.route('/results', methods=['GET'])
def results():
    search_query = request.args.get('q', '')
    search_field = request.args.get('field', 'title')
    search_field_display = search_field[0].upper() + search_field[1:]
    podcasts = services.get_podcasts_filtered(repository.repo_instance, search_field.lower(), search_query)


    # Pagination
    current_page = int(request.args.get('page', 1))# Get the current page number, default is 1

    num_of_podcasts_per_page = 10
    # Calculate total number of podcasts
    total_podcasts = len(podcasts)
    total_pages = math.ceil(total_podcasts/num_of_podcasts_per_page)

    start = (current_page - 1) * num_of_podcasts_per_page  # Calculate the start index
    end = start + num_of_podcasts_per_page  # Calculate the end index

    # Slice the list of podcasts for the current page
    paginated_podcasts = podcasts[start:end]

    has_next = current_page < total_pages
    has_previous = current_page > 1
    next_page = current_page + 1 if has_next else None
    previous_page = current_page - 1 if has_previous else None




    return render_template('search.html', results=paginated_podcasts, query=search_query, field=search_field_display,
                           current_page=current_page,
                           total_pages=total_pages,
                           has_next=has_next,
                           has_previous=has_previous,
                           next_page=next_page,
                           previous_page=previous_page
                           )
