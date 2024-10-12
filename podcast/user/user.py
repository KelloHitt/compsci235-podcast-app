from flask import Blueprint, render_template, request, redirect, url_for, flash

import podcast.adapters.repository as repository
import podcast.user.services as services
import podcast.utilities.utilities as utilities
from podcast.authentication.authentication import login_required

user_blueprint = Blueprint('user_bp', __name__)


@user_blueprint.route('/user/playlist', methods=['GET', 'POST'])
@login_required
def show_user_playlist():
    episodes_in_playlist = []
    try:
        playlist_and_username = services.get_users_playlist(repository.repo_instance)
        playlist = playlist_and_username[0]
        username = playlist_and_username[1]
        playlist_name = f"{username}'s Playlist"
        if playlist:
            episodes_in_playlist = sorted(services.get_episodes_in_playlist(repository.repo_instance, playlist),
                                          key=lambda episode: episode.podcast.title)
    except ValueError as e:
        flash(str(e), 'error')
    episode_page = request.args.get('episode_page', default=1, type=int)
    paginated_episodes, next_episode_page, prev_episode_page, total_pages = (
        utilities.get_episodes_pagination(episodes_in_playlist, episode_page))
    categories = utilities.get_categories()['categories']
    return render_template(
        'user/playlist.html',
        episodes=paginated_episodes,
        categories=categories,
        episode_page=episode_page,
        next_episode_page=next_episode_page,
        prev_episode_page=prev_episode_page,
        total_pages=total_pages,
        episodes_in_playlist=episodes_in_playlist,
        playlist=playlist,
        playlist_name=playlist_name
    )


@user_blueprint.route("/user/playlist/remove_from_playlist", methods=["GET", "POST"])
@login_required
def remove_from_playlist():
    episode_id = request.form.get("episode_id", type=int)
    episode = services.get_episode_by_id(repository.repo_instance, episode_id)
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


@user_blueprint.route('/user/reviews', methods=['GET'])
@login_required
def show_user_reviews():
    user_reviews = []
    page = request.args.get('page', default=1, type=int)
    reviews_per_page = 10
    try:
        user_reviews = services.get_users_reviews(repository.repo_instance)
    except Exception as error:
        flash(str(error), "error")
    total_reviews = len(user_reviews)
    pages_count = (total_reviews + reviews_per_page - 1) // reviews_per_page
    if page < 1:
        page = 1
    if page > pages_count:
        page = pages_count
    start = (page - 1) * reviews_per_page
    end = start + reviews_per_page
    paginated_reviews = user_reviews[start:end]
    categories = utilities.get_categories()['categories']
    return render_template(
        'user/profile.html',
        user_reviews=paginated_reviews,
        current_page=page,
        pages_count=pages_count,
        categories=categories
    )


@user_blueprint.route('/user/delete_review', methods=['POST'])
@login_required
def delete_review():
    review_id = request.form.get("review_id", type=int)
    try:
        services.delete_review(repository.repo_instance, review_id)
        flash(f'Review deleted successfully!', "error")
    except Exception as error:
        flash(str(error), "error")
    return redirect(url_for("user_bp.show_user_reviews"))
