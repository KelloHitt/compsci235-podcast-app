from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Episode, Playlist


def get_categories(repository: AbstractRepository):
    categories = repository.get_categories()
    return categories


def in_playlist(playlist: Playlist, episode: Episode):
    return episode in playlist.episodes
