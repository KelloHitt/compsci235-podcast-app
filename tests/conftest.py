from pathlib import Path

import pytest

import podcast.adapters.repository as repo
from podcast import create_app
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.memory_repository import MemoryRepository
from podcast.adapters.repository_populate import populate_data

TEST_DATA_PATH = Path(__file__).parent / "data"


@pytest.fixture()
def data_path():
    return TEST_DATA_PATH


@pytest.fixture
def csv_reader() -> CSVDataReader:
    csv_reader = CSVDataReader()
    return csv_reader


@pytest.fixture
def in_memory_repo(data_path):
    repo.repo_instance = MemoryRepository()
    populate_data(repo.repo_instance, data_path)
    return repo.repo_instance


@pytest.fixture
def client():
    my_app = create_app(
        {
            "TESTING": True,
            "TEST_DATA_PATH": TEST_DATA_PATH,
            "WTF_CSRF_ENABLED": False,
            "REPOSITORY": "memory",
        }
    )
    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def register(self, username="testUser1", password="testUserpassword1"):
        return self.__client.post(
            "/authentication/register",
            data={"username": username, "password": password},
        )

    def login(self, username="testUser1", password="testUserpassword1"):
        return self.__client.post(
            "/authentication/login",
            data={"username": username, "password": password},
        )

    def logout(self):
        return self.__client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
