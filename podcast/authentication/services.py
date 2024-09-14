from werkzeug.security import generate_password_hash, check_password_hash

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import User, Review, Podcast
from typing import Iterable


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass

class NonExistentPodcastException(Exception):
    pass

def add_user(username: str, password: str, repo: AbstractRepository):
    # Check that the given username is available.
    user = repo.get_user(username)
    if user is not None:
        raise NameNotUniqueException

    # Encrypt password so that the database doesn't store passwords 'in the clear'.
    password_hash = generate_password_hash(password)

    # Create and store the new User, with password encrypted.
    repo.add_user(username, password_hash)


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def authenticate_user(username: str, password: str, repo: AbstractRepository):
    authenticated = False

    user = repo.get_user(username)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException

def add_review(review_id: int, podcast: Podcast, review_description: str, review_rating: int, user: User, repo: AbstractRepository):
    podcast = repo.get_podcast(podcast.id)
    if podcast is None:
        raise NonExistentPodcastException
    user = repo.get_user(user.username)
    if user is None:
        raise UnknownUserException

    review = Review(review_id, podcast, user, review_rating, review_description)
    repo.add_review(review)

def get_reviews_for_podcast(podcast_id, repo: AbstractRepository):
    podcast = repo.get_podcast(podcast_id)
    if podcast is None:
        raise NonExistentPodcastException

    return reviews_to_dict(repo.get_reviews())


# ===================================================
# Functions to convert model entities to dictionaries
# ===================================================

def user_to_dict(user: User):
    user_dict = {
        'username': user.username,
        'password': user.password
    }
    return user_dict

def review_to_dict(review: Review):
    review_dict = {
        'user_name': review.reviewer.username,
        'podcast_id': review.podcast.id,
        'review_description': review.content,
        'review_rating': review.rating
    }
    return review_dict

def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]