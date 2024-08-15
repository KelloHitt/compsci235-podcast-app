from podcast.adapters.repository import AbstractRepository


def get_podcasts_by_page(repository: AbstractRepository, page_number: int):
    page_size = 10  # Each page shows 10 podcasts
    list_of_podcasts = repository.get_podcasts_by_page(page_number, page_size)
    has_next = repository.has_next_page(page_number, page_size)
    has_previous = repository.has_previous_page(page_number)
    next_page = repository.get_next_page(page_number, page_size)
    previous_page = repository.get_previous_page(page_number)

    total_podcasts = repository.get_number_of_podcasts()
    last_page = (total_podcasts + page_size - 1) // page_size

    # Return all the information as dictionary
    return {
        'podcasts': list_of_podcasts,
        'has_next': has_next,
        'has_previous': has_previous,
        'next_page': next_page,
        'previous_page': previous_page,
        'current_page': page_number,
        'last_page': last_page
    }
