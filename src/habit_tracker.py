import datetime


from typing import TypedDict, List, NotRequired, Optional, Literal

Periodicity = Literal["daily", "weekly", "biweekly", "monthly", "yearly"]

class HabitType(TypedDict):
  id: int
  name: str
  description: NotRequired[str]
  periodicity: Periodicity
  creation_date: str 

class CompletionType(TypedDict):
  id: int
  habit_id: int 
  completion_date: str

class HabitTracker:
  habits:List[HabitType] = []
  completions:List[CompletionType] = []

  def __init__(self, initial_habits: Optional[List[HabitType]] = None):
    """Initialize with optional starting habits."""
    self.habits = initial_habits.copy() if initial_habits else []

  def create_habit(self, habit: HabitType) -> None:
    """Add a new habit to the tracker."""
    if not habit.get('id'):
        raise ValueError("Habit must have an 'id' field")
    self.habits.append(habit)

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
    h = next(item for item in self.habits if item.get("id") == id)

    if h is None:
        raise ValueError(f"Habit with id {id} not found.")

    today = datetime.date.today()
    new_id = max((c["id"] for c in self.completions), default=0) + 1
    new_completion: CompletionType = {"habit_id": id, "id": new_id, "completion_date": str(today)}
    self.completions.append(new_completion)
    return new_completion  
