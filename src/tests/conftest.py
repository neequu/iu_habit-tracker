import pytest

from src.database import DB_DIR, init_db
from src.model import CreateHabitBody


@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch, tmp_path):
    """Automatically runs before each test to set up a test database"""
    # Create a temporary database file
    test_db_path = tmp_path / "test_habits.db"

    # Monkeypatch the DB_PATH to use test database
    monkeypatch.setattr("database.DB_PATH", str(test_db_path))

    # Ensure the directory exists
    DB_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize the database
    init_db()

    yield


@pytest.fixture
def habit_factory():
    def _make(**kwargs) -> CreateHabitBody:
        return {
            "name": kwargs.get("name", "Default habit"),
            "description": kwargs.get("description", "Default description"),
            "periodicity": kwargs.get("periodicity", "daily"),
            "start_date": kwargs.get("start_date", "2025-01-01"),
        }

    return _make
