import sqlite3
from typing import Unpack

import pytest

from src.core.model import CreateHabitBody
from src.infra.database import init_db


@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    # Create a shared in-memory connection
    connection = sqlite3.connect(":memory:")
    # Patch get_connection to always return this shared connection
    monkeypatch.setattr("src.infra.database.get_connection", lambda: connection)
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
