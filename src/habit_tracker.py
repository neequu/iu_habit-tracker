import datetime
from typing import List, Optional
from src.model import HabitType, CompletionType, CreateHabitBody
from src.database import add_habit, seed_initial_habits


class HabitTracker:
  def __init__(self, initial_habits: Optional[List[HabitType]] = None) -> None:
    """Initialize with optional starting habits."""
    seed_initial_habits(initial_habits)

  def create_habit(self, habit: CreateHabitBody) -> None:
    """Add a new habit to the tracker."""
    add_habit(habit)

  def delete_habit(self, id: int) -> bool:
    """Remove a habit by ID. Returns True if found and deleted."""
    original_count: int = len(self.habits)
    self.habits = [item for item in self.habits if item.get("id") != id]
    if (not len(self.habits) < original_count):
      return False
    
    self.completions = [item for item in self.completions if item.get("habit_id") != id]
    
    return True
  
  def complete_habit(self, id:int) -> CompletionType:
    """Mark a habit as done. Returns True if habit was found."""
    h: HabitType = next(item for item in self.habits if item.get("id") == id)

    if h is None:
        raise ValueError(f"Habit with id {id} not found.")
    
    # todo: add validation for completion within the same period

    today = datetime.date.today()
    new_id: int = max((c["id"] for c in self.completions), default=0) + 1
    new_completion: CompletionType = {"habit_id": id, "id": new_id, "completion_date": str(today)}
    self.completions.append(new_completion)
    return new_completion  
