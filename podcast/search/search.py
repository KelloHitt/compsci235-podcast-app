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
    podcasts = services.get_podcasts_list(repository)


    # Filter podcasts based on the search criteria
    results = []
    if (search_field == 'category'):
        for podcast in podcasts:
            if (search_field in podcast.categories):
                results.append(podcast)
    elif (search_field == 'title'):
        for podcast in podcasts:
            if (search_field in podcast.title):
                results.append(podcast)
    else:
        for podcast in podcasts:
            if (search_field in podcast.author):
                results.append(podcast)




    return render_template('search.html', results=results, query=search_query, field=search_field)

