import podcast.utilities.utilities as utilities
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Episode, Playlist, User


def get_users_playlist(repository: AbstractRepository):
    username = utilities.get_username()
    playlist = repository.get_users_playlist(username)
    return playlist


def get_episodes_in_playlist(playlist: Playlist):
    return playlist.episodes


def remove_from_playlist(repository: AbstractRepository, episode: Episode):
    username = utilities.get_username()
    user = repository.get_user(username)
    if user is not None:
        user.playlist.delete_episode(episode)


def get_episode_by_id(repository: AbstractRepository, episode_id: int):
    return repository.get_episode(episode_id)


def get_users_reviews(repository: AbstractRepository):
    username = utilities.get_username()
    return repository.get_users_reviews(username)


def delete_review(repository: AbstractRepository, review_id: int):
    repository.delete_review(review_id)
