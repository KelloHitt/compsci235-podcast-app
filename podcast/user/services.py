import podcast.utilities.utilities as utilities
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Episode, Playlist


def get_users_playlist(repository: AbstractRepository):
    username = utilities.get_username()
    playlist = repository.get_users_playlist(username)
    return [playlist, username]


def get_episodes_in_playlist(repository: AbstractRepository, playlist: Playlist):
    return repository.get_episodes_in_playlist(playlist)


def remove_from_playlist(repository: AbstractRepository, episode: Episode):
    username = utilities.get_username()
    user = repository.get_user(username)
    if user is not None:
        repository.remove_from_playlist(username, episode)


def get_episode_by_id(repository: AbstractRepository, episode_id: int):
    return repository.get_episode(episode_id)


def get_users_reviews(repository: AbstractRepository):
    username = utilities.get_username()
    return repository.get_users_reviews(username)


def delete_review(repository: AbstractRepository, review_id: int):
    repository.delete_review(review_id)
