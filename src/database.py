import sqlite3
from datetime import date, timedelta
from pathlib import Path

from src.date_utils import get_period_delta
from src.model import (
    CompletionType,
    CreateCompletionBody,
    CreateHabitBody,
    HabitType,
    Periodicity,
    SortOrder,
)

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

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            periodicity TEXT NOT NULL,
            start_date TEXT NOT NULL
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY,
            habit_id INTEGER NOT NULL,
            completion_date TEXT NOT NULL,
            FOREIGN KEY(habit_id) REFERENCES habits(id) ON DELETE CASCADE
        )
        """
        )

        conn.commit()


def generate_completions(
    habit_id: int, periodicity: Periodicity, start_date: date, week_count=4
) -> list[tuple]:
    """Generate completion data for a habit for given weeks. Default span is 4 weeks."""
    completions: list[tuple] = []
    delta = timedelta(days=get_period_delta(periodicity))
    current_date = start_date - timedelta(weeks=week_count)

    while current_date <= start_date:
        completions.append((habit_id, current_date.isoformat()))
        current_date += delta

    return completions


def seed_initial_habits(initial_habits) -> None:
    """Seeds the database with predefined habits and 4 weeks of completion data."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Check if any habits already exist
        cursor.execute("SELECT COUNT(*) FROM habits")
        count = cursor.fetchone()[0]

        if count > 0:
            return

        # Insert habits
        cursor.executemany(
            """
        INSERT INTO habits (name, description, periodicity, start_date)
        VALUES (?, ?, ?, ?)
        """,
            initial_habits,
        )

        # Get the IDs of the newly inserted habits
        cursor.execute("SELECT id, periodicity, start_date FROM habits")
        habits = cursor.fetchall()

        # Generate and insert completions for each habit
        for habit_id, periodicity, start_date in habits:
            start_date = (
                date.fromisoformat(start_date)
                if isinstance(start_date, str)
                else start_date
            )
            completions = generate_completions(habit_id, periodicity, start_date)

            cursor.executemany(
                """
            INSERT INTO completions (habit_id, completion_date)
            VALUES (?, ?)
            """,
                completions,
            )

        conn.commit()
        print(
            f"Seeded {len(initial_habits)} initial habits with 4 weeks of completion data."
        )


def add_habit(habit: CreateHabitBody) -> int | None:
    """Add a new habit to the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
        INSERT INTO habits (name, description, periodicity, start_date)
        VALUES (?, ?, ?, ?)
        """,
            (
                habit["name"],
                habit.get("description", ""),
                habit["periodicity"],
                habit["start_date"],
            ),
        )
        conn.commit()
        return cursor.lastrowid


def query_habits() -> list[HabitType]:
    """Retrieve all habits from the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, description, periodicity, start_date FROM habits"
        )
        rows = cursor.fetchall()
        return [parse_habit_row(row) for row in rows]


def query_habit_by_id(habit_id: int) -> HabitType | None:
    """Retrieve a single habit by its ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT id, name, description, periodicity, start_date
        FROM habits WHERE id = ?
        """,
            (habit_id,),
        )
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
        cursor.execute(
            """
        SELECT id, name, description, periodicity, start_date 
        FROM habits 
        WHERE periodicity = ?
        
        """,
            (period,),
        )
        rows = cursor.fetchall()
        return [parse_habit_row(row) for row in rows]


def query_completions_by_habit_id(
    habit_id: int, order: SortOrder = "ASC"
) -> list[CompletionType]:
    """Retrieve completions for a habit by habit's ID."""
    order_clause = "ASC" if order == "ASC" else "DESC"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT id, habit_id, completion_date
            FROM completions 
            WHERE habit_id = ?
            ORDER BY completion_date {order_clause}
        """,
            (habit_id,),
        )
        return [
            {"id": row[0], "habit_id": row[1], "completion_date": row[2]}
            for row in cursor.fetchall()
        ]


def query_latest_completion_by_habit_id(habit_id: int) -> CompletionType | None:
    """Retrieves the most recent completion for a habit, or None if none exists."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, habit_id, completion_date
            FROM completions
            WHERE habit_id = ?
            ORDER BY completion_date DESC
            LIMIT 1
        """,
            (habit_id,),
        )
        row = cursor.fetchone()
        return (
            {"id": row[0], "habit_id": row[1], "completion_date": row[2]}
            if row
            else None
        )


def add_completion(completion: CreateCompletionBody) -> int | None:
    """Add a habit completion entry to the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO completions (habit_id, completion_date)
            VALUES (?, ?)
        """,
            (
                completion["habit_id"],
                completion["completion_date"],
            ),
        )
        conn.commit()
        return cursor.lastrowid
