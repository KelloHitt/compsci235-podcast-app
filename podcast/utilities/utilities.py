from flask import session

import podcast.adapters.repository as repository
import podcast.utilities.services as services


def get_categories():
    categories = services.get_categories(repository.repo_instance)
    return {'categories': categories}


def get_username():
    username = None
    if "username" in session:
        username = session["username"]
    return username
