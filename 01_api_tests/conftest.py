# conftest.py — общие фикстуры для API-тестов

import pytest
import requests


BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api_client():
    """Сессия для запросов с общими заголовками."""
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    yield session
    session.close()


@pytest.fixture
def base_url():
    return BASE_URL