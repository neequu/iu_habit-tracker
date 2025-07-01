import sqlite3
from pathlib import Path
from src.model import HabitType, CreateHabitBody, Periodicity, CompletionType, CreateCompletionBody
from typing import Literal

SortOrder = Literal["ASC", "DESC"]

DB_DIR = Path(__file__).parent 
DB_PATH = DB_DIR / "habits.db"

def parse_habit_row(row: tuple) -> HabitType:
    return {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "periodicity": row[3],
        "start_date": row[4],
    }

def get_connection() -> sqlite3.Connection:
    """Ensure directory and return connection."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db() -> None:
    """Creates tables if they don't exist."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            periodicity TEXT NOT NULL,
            start_date TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY,
            habit_id INTEGER NOT NULL,
            completion_date TEXT NOT NULL,
            FOREIGN KEY(habit_id) REFERENCES habits(id) ON DELETE CASCADE
        )
        """)

        conn.commit()

def seed_initial_habits(initial_habits) -> None:
    """Seeds the database with predefined habits if none exist."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # check if any habits already exist
        cursor.execute("SELECT COUNT(*) FROM habits")
        count = cursor.fetchone()[0]

        if count > 0:
            print("Habits already seeded.")
            return

        cursor.executemany("""
        INSERT INTO habits (name, description, periodicity, start_date)
        VALUES (?, ?, ?, ?)
        """, initial_habits)

        conn.commit()
        print(f"Seeded {len(initial_habits)} initial habits.")       



def add_habit(habit: CreateHabitBody) -> int | None:
    """Add a new habit to the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO habits (name, description, periodicity, start_date)
        VALUES (?, ?, ?, ?)
        """, (
            habit["name"],
            habit.get("description", ""),
            habit["periodicity"],
            habit["start_date"],
        ))
        conn.commit()
        return cursor.lastrowid

def query_habits() -> list[HabitType]:
    """Retrieve all habits from the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description, periodicity, start_date FROM habits")
        rows = cursor.fetchall()
        return [parse_habit_row(row) for row in rows]


def query_habit_by_id(habit_id: int) -> HabitType | None:
    """Retrieve a single habit by its ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, name, description, periodicity, start_date
        FROM habits WHERE id = ?
        """, (habit_id,))
        row = cursor.fetchone()
        if row:
            return parse_habit_row(row)
        return None
  
def delete_habit_by_id(habit_id: int) -> bool:
    """Delete a habit by its ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        conn.commit()
        return cursor.rowcount > 0


def query_habits_by_period(period: Periodicity) -> list[HabitType]:
    """Retrieve all habits from the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, name, description, periodicity, start_date 
        FROM habits 
        WHERE periodicity = ?
        
        """, (period,))
        rows = cursor.fetchall()
        return [parse_habit_row(row) for row in rows]


def query_completions_by_habit_id(habit_id: int, order: SortOrder = "ASC") -> list[CompletionType]:
    """Retrieve completions for a habit by habit's ID."""
    order_clause = "ASC" if order == "ASC" else "DESC"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT id, habit_id, completion_date
            FROM completions 
            WHERE habit_id = ?
            ORDER BY completion_date {order_clause}
        """, (habit_id,))
        return [
            {"id": row[0], "habit_id": row[1], "completion_date": row[2]}
            for row in cursor.fetchall()
        ]

def query_latest_completion(habit_id: int) -> CompletionType | None:
    """Retrieves the most recent completion for a habit, or None if none exists."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, habit_id, completion_date
            FROM completions
            WHERE habit_id = ?
            ORDER BY completion_date DESC
            LIMIT 1
        """, (habit_id,))
        row = cursor.fetchone()
        return (
            {"id": row[0], "habit_id": row[1], "completion_date": row[2]}
            if row else None
        )


def add_completion(habit_id: int, completion_date: str) -> int | None:
    """Add a habit completion entry to the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO completions (habit_id, completion_date)
            VALUES (?, ?)
        """, (
            habit_id,
            completion_date,
        ))
        conn.commit()
        return cursor.lastrowid