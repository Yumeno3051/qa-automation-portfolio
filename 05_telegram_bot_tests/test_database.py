# test_database.py
"""
Тесты для работы с SQLite-базой (аналог БД Telegram-бота).
Проверяют CRUD-операции, уникальность, связи.
"""

import sqlite3
import pytest


@pytest.fixture
def db():
    """Создаёт тестовую БД в памяти — быстро и без мусора."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT UNIQUE NOT NULL,
            chat_link TEXT NOT NULL
        )
    """)
    conn.commit()

    yield conn

    conn.close()


def add_city(conn, city, link):
    """Утилита для добавления города."""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cities (city, chat_link) VALUES (?, ?)",
        (city, link)
    )
    conn.commit()


def find_city(conn, query):
    """Поиск по частичному совпадению."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT city, chat_link FROM cities WHERE city LIKE ?",
        (f"%{query}%",)
    )
    return cursor.fetchall()


class TestAddCity:
    def test_add_city(self, db):
        """Успешное добавление города."""
        add_city(db, "Москва", "https://t.me/moscow")

        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM cities")
        assert cursor.fetchone()[0] == 1

    def test_add_duplicate_city(self, db):
        """Дубликат города вызывает IntegrityError (UNIQUE)."""
        add_city(db, "Москва", "https://t.me/moscow")

        with pytest.raises(sqlite3.IntegrityError):
            add_city(db, "Москва", "https://t.me/other")


class TestFindCity:
    def test_find_exact(self, db):
        """Точное совпадение."""
        add_city(db, "Москва", "https://t.me/moscow")
        add_city(db, "Санкт-Петербург", "https://t.me/spb")

        results = find_city(db, "Москва")
        assert len(results) == 1
        assert results[0][0] == "Москва"

    def test_find_partial(self, db):
        """Частичное совпадение."""
        add_city(db, "Москва", "https://t.me/moscow")
        add_city(db, "Московская область", "https://t.me/mo")

        results = find_city(db, "Моск")
        assert len(results) == 2

    def test_find_not_found(self, db):
        """Несуществующий город."""
        add_city(db, "Москва", "https://t.me/moscow")

        results = find_city(db, "Казань")
        assert len(results) == 0