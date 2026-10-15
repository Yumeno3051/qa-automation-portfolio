# test_jsonplaceholder.py
"""
API-тесты для jsonplaceholder.typicode.com — публичного API
для тестирования. Не требует авторизации.

Покрываемые сценарии:
- GET запросы (получение данных)
- POST запросы (создание)
- PUT запросы (обновление)
- DELETE запросы (удаление)
- Проверка статус-кодов
- Проверка структуры ответа
"""

import pytest
import requests


class TestPosts:
    """Тесты для ресурса /posts."""

    def test_get_all_posts(self, api_client, base_url):
        """GET /posts — получение всех постов."""
        response = api_client.get(f"{base_url}/posts")

        assert response.status_code == 200, \
            f"Ожидался 200, получен {response.status_code}"
        assert isinstance(response.json(), list)
        assert len(response.json()) == 100  # у jsonplaceholder 100 постов

    def test_get_post_by_id(self, api_client, base_url):
        """GET /posts/1 — получение поста по ID."""
        response = api_client.get(f"{base_url}/posts/1")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "title" in data
        assert "body" in data
        assert "userId" in data

    def test_get_nonexistent_post(self, api_client, base_url):
        """GET /posts/9999 — несуществующий пост возвращает 404."""
        response = api_client.get(f"{base_url}/posts/9999")

        assert response.status_code == 404

    def test_create_post(self, api_client, base_url):
        """POST /posts — создание нового поста."""
        payload = {
            "title": "Test Post",
            "body": "This is a test",
            "userId": 1
        }
        response = api_client.post(f"{base_url}/posts", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Post"
        assert data["body"] == "This is a test"
        assert "id" in data  # сервер присваивает ID

    def test_update_post(self, api_client, base_url):
        """PUT /posts/1 — обновление поста."""
        payload = {"id": 1, "title": "Updated", "body": "Updated", "userId": 1}
        response = api_client.put(f"{base_url}/posts/1", json=payload)

        assert response.status_code == 200
        assert response.json()["title"] == "Updated"

    def test_delete_post(self, api_client, base_url):
        """DELETE /posts/1 — удаление поста."""
        response = api_client.delete(f"{base_url}/posts/1")

        assert response.status_code == 200


class TestUsers:
    """Тесты для ресурса /users."""

    def test_get_all_users(self, api_client, base_url):
        """GET /users — получение всех пользователей."""
        response = api_client.get(f"{base_url}/users")

        assert response.status_code == 200
        users = response.json()
        assert len(users) == 10

    def test_user_structure(self, api_client, base_url):
        """Проверка структуры пользователя."""
        response = api_client.get(f"{base_url}/users/1")
        user = response.json()

        required_fields = ["id", "name", "username", "email", "address", "phone"]
        for field in required_fields:
            assert field in user, f"Поле '{field}' отсутствует в ответе"

    def test_filter_posts_by_user(self, api_client, base_url):
        """GET /posts?userId=1 — фильтрация постов по пользователю."""
        response = api_client.get(f"{base_url}/posts", params={"userId": 1})

        assert response.status_code == 200
        posts = response.json()
        assert len(posts) == 10
        for post in posts:
            assert post["userId"] == 1


class TestNegative:
    """Негативные тесты."""

    def test_invalid_endpoint(self, api_client, base_url):
        """GET /invalid — несуществующий эндпоинт."""
        response = api_client.get(f"{base_url}/invalid_endpoint")

        assert response.status_code == 404

    def test_wrong_method(self, api_client, base_url):
        """PATCH на неподдерживаемый эндпоинт."""
        response = api_client.patch(f"{base_url}/users/1", json={"name": "Test"})

        # jsonplaceholder принимает PATCH, но проверим, что не 500
        assert response.status_code in (200, 405)