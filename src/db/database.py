import sqlite3
from pathlib import Path
from ..main import habit, get_habits
from models import HabitType

DB_DIR = Path(__file__).parent 
DB_PATH = DB_DIR / "habits.db"


def get_connection() -> sqlite3.Connection:
    """Ensure directory and return connection."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    """Creates tables if they don't exist."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            periodicity TEXT NOT NULL,
            creation_date TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY,
            habit_id INTEGER NOT NULL,
            completion_date TEXT NOT NULL,
            FOREIGN KEY(habit_id) REFERENCES habits(id)
        )
        """)

        conn.commit()



import datetime

def seed_initial_habits() -> None:
    """Seeds the database with 5 predefined habits if none exist."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Check if any habits already exist
        cursor.execute("SELECT COUNT(*) FROM habits")
        count = cursor.fetchone()[0]

        if count > 0:
            print("Habits already seeded.")
            return

        # Today's date
        today = datetime.date.today().isoformat()

        # Predefined habits (at least 1 daily, 1 weekly)
        habits = [
            ("Drink Water", "Stay hydrated by drinking 8 glasses", "daily", today),
            ("Exercise", "Do 20 minutes of physical activity", "daily", today),
            ("Read Book", "Read 10 pages of a book", "daily", today),
            ("Call Parents", "Weekly call to family", "weekly", today),
            ("Clean Room", "Tidy and organize living space", "weekly", today),
        ]

        cursor.executemany("""
        INSERT INTO habits (name, description, periodicity, creation_date)
        VALUES (?, ?, ?, ?)
        """, habits)

        conn.commit()
        print("Seeded 5 initial habits.")       



def add_habit(habit: HabitType) -> int | None:
    """Add a new habit to the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO habits (name, description, periodicity, creation_date)
        VALUES (?, ?, ?, ?)
        """, (
            habit["name"],
            habit.get("description", ""),
            habit["periodicity"],
            habit["creation_date"],
        ))
        conn.commit()
        return cursor.lastrowid

def get_all_habits() -> list[HabitType]:
    """Retrieve all habits from the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description, periodicity, creation_date FROM habits")
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "periodicity": row[3],
                "creation_date": row[4],
            }
            for row in rows
        ]

def get_habit_by_id(habit_id: int) -> dict | None:
    """Retrieve a single habit by its ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, name, description, periodicity, creation_date
        FROM habits WHERE id = ?
        """, (habit_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "periodicity": row[3],
                "creation_date": row[4],
            }
        return None



