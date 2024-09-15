from flask import Blueprint, render_template, request, redirect, url_for, flash

import podcast.adapters.repository as repository
import podcast.user.services as services
import podcast.utilities.utilities as utilities
from podcast.authentication.authentication import login_required

user_blueprint = Blueprint('user_bp', __name__)


@user_blueprint.route('/user/playlist', methods=['GET', 'POST'])
def show_user_playlist():
    playlist = None
    episodes_in_playlist = []
    try:
        playlist = services.get_users_playlist(repository.repo_instance)
        episodes_in_playlist = sorted(services.get_episodes_in_playlist(playlist),
                                      key=lambda episode: episode.podcast.title)
    except ValueError as e:
        flash(str(e), 'error')
    episodes_count = len(episodes_in_playlist)
    episode_page = request.args.get('episode_page', default=1, type=int)
    episodes_per_page = 10
    pages_count = (episodes_count + episodes_per_page - 1) // episodes_per_page
    if episode_page < 1:
        episode_page = 1
    if episode_page > pages_count:
        episode_page = pages_count
    start = (episode_page - 1) * episodes_per_page
    end = start + episodes_per_page
    paginated_episodes = episodes_in_playlist[start:end]
    next_episode_page = episode_page + 1 if end < episodes_count else None
    prev_episode_page = episode_page - 1 if start > 0 else None
    categories = utilities.get_categories()['categories']
    return render_template(
        'user/playlist.html',
        episodes=paginated_episodes,
        categories=categories,
        episode_page=episode_page,
        next_episode_page=next_episode_page,
        prev_episode_page=prev_episode_page,
        total_pages=pages_count,
        episodes_in_playlist=episodes_in_playlist,
        playlist=playlist
    )


@user_blueprint.route("/user/playlist/remove_from_playlist", methods=["GET", "POST"])
@login_required
def remove_from_playlist():
    episode_id = request.form.get("episode_id")
    episode = services.get_episode_by_id(repository.repo_instance, int(episode_id))
    try:
        services.remove_from_playlist(repository.repo_instance, episode)
        flash(f'Episode "{episode.title}" removed from playlist successfully!', "error")
    except Exception as error:
        flash(str(error), "error")
    return redirect(url_for("user_bp.show_user_playlist", podcast_id=episode.podcast.id))


@user_blueprint.route("/user/playlist/remove_all_from_playlist", methods=["GET", "POST"])
@login_required
def remove_all_from_playlist():
    try:
        playlist = services.get_users_playlist(repository.repo_instance)
        if playlist:
            for episode in list(playlist.episodes):
                services.remove_from_playlist(repository.repo_instance, episode)
            flash("All episodes removed from playlist successfully!", "success")
        else:
            flash("Playlist not found for the user.", "error")
    except Exception as error:
        flash(str(error), "error")
    return redirect(url_for("user_bp.show_user_playlist"))
