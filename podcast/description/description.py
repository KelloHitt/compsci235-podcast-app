from flask import Blueprint, render_template, request

import podcast.adapters.repository as repository
import podcast.description.services as services
import podcast.utilities.utilities as utilities

description_blueprint = Blueprint('description_bp', __name__)


@description_blueprint.route('/description', methods=['GET'])
def show_description():
    podcast_id = request.args.get('podcast_id', default=1, type=int)

    # Ensure podcast_id is within valid range
    if podcast_id > 1000:
        podcast_id = 1000
    if podcast_id < 1:
        podcast_id = 1

    # Episode pagination
    episode_page = request.args.get('episode_page', default=1, type=int)
    episodes_per_page = 10

    podcast = services.get_podcast_by_id(repository.repo_instance, podcast_id)
    all_episodes = sorted(podcast.episodes, key=lambda episode: episode.date)

    # Calculate the total number of pages
    total_episodes = len(all_episodes)
    total_pages = (total_episodes + episodes_per_page - 1) // episodes_per_page  # This ensures rounding up

    # Ensure episode_page is within the valid range
    if episode_page < 1:
        episode_page = 1
    if episode_page > total_pages:
        episode_page = total_pages

    # Paginate episodes
    start = (episode_page - 1) * episodes_per_page
    end = start + episodes_per_page
    paginated_episodes = all_episodes[start:end]

    # Determine if there are next or previous pages for episodes
    next_episode_page = episode_page + 1 if end < total_episodes else None
    prev_episode_page = episode_page - 1 if start > 0 else None

    categories = utilities.get_categories()['categories']

    return render_template(
        'podcastDescription.html',
        podcast=podcast,
        episodes=paginated_episodes,
        categories=categories,
        episode_page=episode_page,
        next_episode_page=next_episode_page,
        prev_episode_page=prev_episode_page,
        total_pages=total_pages
    )
