import podcast.adapters.repository as repository
import podcast.utilities.services as services


def get_categories():
    categories = services.get_categories(repository.repo_instance)
    return {'categories': categories}
