import sqlite3
from typing import Unpack

import pytest

from src.database import DB_DIR, init_db
from src.model import CreateHabitBody


@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    # Create a shared in-memory connection
    connection = sqlite3.connect(":memory:")
    # Patch get_connection to always return this shared connection
    monkeypatch.setattr("src.database.get_connection", lambda: connection)
    # Initialize schema on this connection
    init_db()

    yield
    # Close the shared connection after all tests
    connection.close()


@pytest.fixture
def habit_factory():
    def _make(**kwargs: Unpack[CreateHabitBody]) -> CreateHabitBody:
        return {
            "name": kwargs.get("name", "Default habit"),
            "description": kwargs.get("description", "Default description"),
            "periodicity": kwargs.get("periodicity", "daily"),
            "start_date": kwargs.get("start_date", "2025-01-01"),
        }

    return _make
