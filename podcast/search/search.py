from flask import Blueprint, render_template, request
import podcast.adapters.repository as repository
import podcast.search.services as services

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
    podcasts = services.get_podcasts_filtered(repository.repo_instance, search_query)

    # Pagination
    page = request.args.get('page', 1, type=int)  # Get the current page number, default is 1
    per_page = 10
    # Calculate total number of podcasts
    total_podcasts = len(podcasts)
    total_pages = (total_podcasts + per_page - 1)

    # Ensure the page number is within range
    if page > total_pages:
        page = total_pages
    if page < 1:
        page = 1
    # Calculate the slice start and end indices
    start = (page - 1) * per_page
    end = start + per_page
    # Slice the podcasts list to get only the items for the current page
    paginated_podcasts = podcasts[start:end]
    return render_template('search.html', results=paginated_podcasts, query=search_query, field=search_field_display,
                           page=page, total_pages=total_pages,
                           total_podcasts=total_podcasts)
