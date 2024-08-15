from podcast.adapters.repository import AbstractRepository


def get_podcast_by_id(repository: AbstractRepository, podcast_id: int):
    podcast = repository.get_podcast(podcast_id)
    return podcast
