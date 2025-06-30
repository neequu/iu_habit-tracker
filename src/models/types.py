from typing import TypedDict, NotRequired, Literal

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