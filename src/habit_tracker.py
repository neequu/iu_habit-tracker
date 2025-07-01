import datetime
from typing import List, Optional
from src.model import HabitType, CompletionType, CreateHabitBody
from src.database import add_habit, seed_initial_habits, delete_habit_by_id, query_habit_by_id, query_completions_by_habit_id, add_completion, query_latest_completion
from src.dates import parse_date, get_period_delta


class HabitTracker:
  def __init__(self, initial_habits: Optional[List[HabitType]] = None) -> None:
    """Initialize with optional starting habits."""
    # seed_initial_habits(initial_habits)
    pass

  def create_habit(self, habit: CreateHabitBody) -> int | None:
    """Add a new habit to the tracker."""
    return add_habit(habit)

  def delete_habit(self, id: int) -> bool:
    """Remove a habit by ID. Returns True if found and deleted."""
    return delete_habit_by_id(id)
  
  def complete_habit(self, id:int) -> int | None:
    """Mark a habit as done. Returns True if habit was found."""
    habit = query_habit_by_id(id)

    if habit is None:
        raise ValueError(f"Habit with id {id} not found.")
    
    today = datetime.date.today()
    latest_completion = query_latest_completion(id)

    if latest_completion:
        last_date = parse_date(latest_completion["completion_date"])
        period_delta = get_period_delta(habit["periodicity"])
        if (today - last_date).days < period_delta:
            raise ValueError("Cannot complete habit twice in the same period.")

    return add_completion(habit['id'], today.isoformat())  
