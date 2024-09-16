from flask import Blueprint, render_template, request
import podcast.adapters.repository as repository
import podcast.search.services as services
import podcast.utilities.utilities as utilities

search_blueprint = Blueprint(
    'search_bp', __name__)


@search_blueprint.route('/search', methods=['GET'])
def search():
    return render_template('search.html')


@search_blueprint.route('/results', methods=['GET'])
def results():
    search_query = request.args.get('q', '')
    search_field = request.args.get('field', 'title')


    podcasts = services.get_podcasts_filtered(repository.repo_instance, search_query)


    return render_template('search.html', results=podcasts, query=search_query, field=search_field)


