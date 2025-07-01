from typing import Literal, NotRequired, TypedDict

Periodicity = Literal["daily", "weekly", "biweekly"]
SortOrder = Literal["ASC", "DESC"]


class HabitType(TypedDict):
    id: int
    name: str
    description: NotRequired[str]
    periodicity: Periodicity
    start_date: str


class CreateHabitBody(TypedDict):
    name: str
    description: NotRequired[str]
    periodicity: Periodicity
    start_date: str


class CompletionType(TypedDict):
    id: int
    habit_id: int
    completion_date: str


class CreateCompletionBody(TypedDict):
    habit_id: int
    completion_date: str
