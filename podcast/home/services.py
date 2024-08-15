import random
from typing import List

from podcast.adapters.repository import AbstractRepository


def get_random_podcasts_info(repository: AbstractRepository, number_of_podcasts: int = 12) -> List:
    """ Randomly choose 12 podcasts to display on the home page """
    total_podcasts = repository.get_number_of_podcasts()

    # Randomly select podcast IDs
    podcast_ids = random.sample(range(1, total_podcasts + 1), number_of_podcasts)

    # Retrieve the podcasts and collect the required information
    podcast_dicts = []

    for podcast_id in podcast_ids:
        podcast = repository.get_podcast(podcast_id)
        podcast_dict = {
            "id": podcast_id,
            "title": podcast.title,
            "image_url": podcast.image,
            "author_name": podcast.author.name
        }
        podcast_dicts.append(podcast_dict)

    return podcast_dicts
