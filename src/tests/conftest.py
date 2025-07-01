import pytest

from src.database import DB_DIR, init_db


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
