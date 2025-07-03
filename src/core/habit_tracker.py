import datetime

from src.core.model import CreateHabitBody
from src.infra.database import (
    add_completion,
    add_habit,
    delete_habit_by_id,
    query_habit_by_id,
    query_latest_completion_by_habit_id,
)
from src.infra.date_utils import get_period_delta, parse_date
from src.infra.initialization import init_app


class HabitTracker:
    def __init__(self) -> None:
        """Calls the initialization function to prepare app environment."""
        init_app()

    def create_habit(self, habit: CreateHabitBody) -> int | None:
        """Creates and stores a new habit in the tracker.

        Args:
            habit (CreateHabitBody): Dictionary containing habit details including:
                - name: str
                - periodicity: str (daily/weekly/biweekly)
                - description: Optional[str]
                - creation_date: str (ISO format)

        Returns:
            int | None: ID of the newly created habit, or None if creation failed
        """
        return add_habit(habit)

    def delete_habit(self, id: int) -> bool:
        """Permanently removes a habit from the tracker.

        Args:
            id (int): The ID of the habit to delete

        Returns:
            bool: True if habit was found and deleted, False otherwise

        Note:
            This will also delete all completion records associated with the habit.
        """
        return delete_habit_by_id(id)

    def complete_habit(self, id: int) -> int | None:
        """Records a completion of the specified habit.

        Args:
            id (int): The ID of the habit to complete

        Returns:
            int | None: ID of the new completion record, or None if failed

        Raises:
            ValueError: If either:
                - No habit exists with the given ID
                - Habit was already completed in current period

        Note:
            Completion is only allowed once per period (day/week/biweek).
        """
        habit = query_habit_by_id(id)

        if habit is None:
            raise ValueError(f"Habit with id {id} not found.")

        today = datetime.date.today()
        latest_completion = query_latest_completion_by_habit_id(id)

        if latest_completion:
            last_date = parse_date(latest_completion["completion_date"])
            period_delta = get_period_delta(habit["periodicity"])
            if (today - last_date).days < period_delta:
                raise ValueError("Cannot complete habit twice in the same period.")

        return add_completion(
            {
                "completion_date": today.isoformat(),
                "habit_id": habit["id"],
            }
        )
