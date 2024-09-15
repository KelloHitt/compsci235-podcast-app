from flask import Blueprint, render_template, request, redirect, url_for, flash

import podcast.adapters.repository as repository
import podcast.description.services as services
import podcast.utilities.utilities as utilities
from podcast.authentication.authentication import login_required

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

    # Get the logged-in user's playlist
    playlist = services.get_playlist(repository.repo_instance)

    # Check if episodes are in the playlist using in_playlist method
    episodes_in_playlist = set()
    if playlist:
        for episode in paginated_episodes:
            if services.in_playlist(playlist, episode):
                episodes_in_playlist.add(episode.id)

    return render_template(
        'podcastDescription.html',
        podcast=podcast,
        episodes=paginated_episodes,
        categories=categories,
        episode_page=episode_page,
        next_episode_page=next_episode_page,
        prev_episode_page=prev_episode_page,
        total_pages=total_pages,
        episodes_in_playlist=episodes_in_playlist
    )


@description_blueprint.route("/add_to_playlist", methods=["GET", "POST"])
@login_required
def add_to_playlist():
    episode_id = request.form.get("episode_id")
    episode = services.get_episode_by_id(repository.repo_instance, int(episode_id))
    try:
        services.add_to_playlist(repository.repo_instance, episode)
        flash(f'Episode "{episode.title}" added to playlist successfully!', "success")
    except Exception as error:
        flash(str(error), "error")
    return redirect(url_for("description_bp.show_description", podcast_id=episode.podcast.id))


@description_blueprint.route("/remove_from_playlist", methods=["GET", "POST"])
@login_required
def remove_from_playlist():
    episode_id = request.form.get("episode_id")
    episode = services.get_episode_by_id(repository.repo_instance, int(episode_id))
    try:
        services.remove_from_playlist(repository.repo_instance, episode)
        flash(f'Episode "{episode.title}" removed from playlist successfully!', "error")
    except Exception as error:
        flash(str(error), "error")
    return redirect(url_for("description_bp.show_description", podcast_id=episode.podcast.id))


@description_blueprint.route('/add_all_to_playlist', methods=['POST'])
@login_required
def add_all_to_playlist():
    podcast_id = request.form.get('podcast_id', type=int)
    podcast = services.get_podcast_by_id(repository.repo_instance, podcast_id)
    all_episodes = podcast.episodes
    try:
        for episode in all_episodes:
            services.add_to_playlist(repository.repo_instance, episode)
        flash(f'All episodes in the podcast added to playlist successfully!', "success")
    except Exception as error:
        flash(str(error), "error")
    return redirect(url_for('description_bp.show_description', podcast_id=podcast_id))
