from typing import List

from flask import session

import podcast.adapters.repository as repository
import podcast.utilities.services as services
from podcast.domainmodel.model import Episode, Review, Playlist


def get_categories():
    categories = services.get_categories(repository.repo_instance)
    return {'categories': categories}


def get_username():
    username = None
    if "username" in session:
        username = session["username"]
    return username


def get_episodes_pagination(all_episodes: List[Episode], episode_page: int):
    # Calculate the total number of pages
    total_episodes = len(all_episodes)
    episodes_per_page = 10
    total_pages = (total_episodes + episodes_per_page - 1) // episodes_per_page

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

    return paginated_episodes, next_episode_page, prev_episode_page, total_pages


def calculate_average_rating(reviews: List[Review]):
    if reviews:
        average_rating = sum(review.rating for review in reviews) / len(reviews)
    else:
        average_rating = 0  # Set default value to 0 if there are no reviews
    return average_rating


def get_episodes_in_playlist(paginated_episodes: List[Episode], playlist: Playlist):
    # Check if episodes are in the playlist using in_playlist method
    episodes_in_playlist = set()
    if playlist:
        for episode in paginated_episodes:
            if services.in_playlist(playlist, episode):
                episodes_in_playlist.add(episode.id)
    return episodes_in_playlist
