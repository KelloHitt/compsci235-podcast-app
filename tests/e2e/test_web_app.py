from unittest.mock import patch

import pytest
from flask import session


def test_register(client):
    response_code = client.get("/authentication/register").status_code
    assert response_code == 200

    response = client.post("/authentication/register", data={"username": "testUser1", "password": "testUserpassword1"})
    assert response.headers["Location"] == "/authentication/login"


@pytest.mark.parametrize(
    ('username', 'password', 'message'),
    (
            ('', '', b'Your username is required'),
            ('cj', '', b'Your username is too short'),
            ('test', '', b'Your password is required'),
            ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
            ("testUser1", "testUserpassword1", b"Your username is already taken - please try another one."),
    ))
def test_register_with_invalid_input(auth, client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    auth.register()  # register a user
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    with patch('podcast.home.services.get_random_podcasts_info') as mock_get_podcasts:
        mock_get_podcasts.return_value = []  # Simulate an empty list of podcasts
        # create user
        response = auth.register()
        # check if redirects to login page
        assert response.headers["Location"] == "/authentication/login"
        # Check that we can retrieve the login page
        status_code = client.get('/authentication/login').status_code
        assert status_code == 200
        # test login
        response = auth.login()
        # test if successful and redirected to home page
        assert response.headers["Location"] == "/"
        # Check that a session has been created for the logged-in user.
        with client:
            client.get('/')
            assert session['username'] == "testUser1"


def test_logout(client, auth):
    # Login a user.
    auth.login()
    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    with patch('podcast.home.services.get_random_podcasts_info') as mock_get_podcasts:
        mock_get_podcasts.return_value = []  # Simulate an empty list of podcasts
        response = client.get("/")
        assert response.status_code == 200
        assert b"Editor's Pick:" in response.data


def test_login_required_to_review(client):
    response = client.post("/add_review")
    assert response.headers["Location"] == "/authentication/login"


def test_review_valid(client, auth):
    auth.register()
    auth.login()

    response = client.get("/description", query_string={"podcast_id": 1})
    assert response.status_code == 200  # Check if the page loads successfully

    response = client.post("/add_review", data={"description": "Who likes this game??", "rating": 1, "podcast_id": 1})
    assert response.status_code == 302  # Check for redirection status
    assert response.headers["Location"] == "/description?podcast_id=1"  # Redirect to the same podcast description page


@pytest.mark.parametrize(
    ("description", "rating", "messages"),
    (
        ("fuck this game its bad?", 3, b"Your comment must not contain profanity!"),
        (" ", 1, b"Comment is required."),
        ("wa", 3, b"Your comment is too short."),
    ),
)
def test_review_game_with_invalid_input(client, auth, description, rating, messages):
    auth.register()
    auth.login()
    response = client.post("/add_review", data={"description": description, "rating": rating, "podcast_id": 1})
    for message in messages:
        assert message in response.data


def test_add_to_playlist_login_required(client, auth):
    pass


def test_show_all_playlists(client, auth):
    pass


def test_podcast_no_reviews(client):
    pass


def test_podcast_with_reviews(client):
    pass


def test_podcasts_by_pages(client):
    pass


def test_podcasts_by_categories_pages(client):
    pass
