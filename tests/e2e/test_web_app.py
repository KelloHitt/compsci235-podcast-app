# TODO: This file is for Integration testing


import pytest
from flask import session


def test_register(client):
    pass


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        # TODO: set up testing parameters
    ),
)
def test_register_with_invalid_input(client, username, password, message):
    pass


def test_login(client, auth):
    pass


def test_logout(client, auth):
    pass


def test_index(client):
    pass


def test_login_required_to_review(client):
    pass


def test_review_valid(client, auth):
    pass


@pytest.mark.parametrize(
    ("comment", "rating", "messages"),
    (
        # TODO: set up testing parameters
    ),
)
def test_review_with_invalid_input(client, auth, comment, rating, messages):
    pass


def test_add_to_playlist_login_required(client, auth):
    pass


def test_show_all_playlists(client, auth):
    pass


def test_podcast_no_reviews(client):
    pass


def test_game_wtih_reviews(client):
    pass


def test_podcasts_by_pages(client):
    pass


def test_podcasts_by_categories_pages(client):
    pass
