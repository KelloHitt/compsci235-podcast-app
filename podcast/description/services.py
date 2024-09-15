import podcast.utilities.utilities as utilities
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Episode, Playlist


def get_podcast_by_id(repository: AbstractRepository, podcast_id: int):
    podcast = repository.get_podcast(podcast_id)
    return podcast


def get_episode_by_id(repository: AbstractRepository, episode_id: int):
    return repository.get_episode(episode_id)


def add_to_playlist(repository: AbstractRepository, episode: Episode):
    username = utilities.get_username()
    repository.add_to_playlist(username, episode)


def get_playlist(repository: AbstractRepository):
    username = utilities.get_username()
    user = repository.get_user(username)
    return user.playlist if user is not None else None


def in_playlist(playlist: Playlist, episode: Episode):
    return episode in playlist.episodes


def remove_from_playlist(repository: AbstractRepository, episode: Episode):
    username = utilities.get_username()
    user = repository.get_user(username)
    if user is not None:
        user.playlist.delete_episode(episode)