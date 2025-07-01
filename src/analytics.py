from .model import HabitType, Periodicity
from src.database import query_habits, query_habits_by_period, query_completions_by_habit_id, query_habit_by_id
from src.dates import get_period_delta, parse_date

def get_habits_by_period(period: Periodicity) -> list[HabitType]:
  """Get habits by period."""
  return query_habits_by_period(period)

def get_habits() -> list[HabitType]:
  """"Get all habits"""
  return query_habits()

def get_longest_streak_by_id(habit_id: int) -> int:
    """"Get the longest streak of a single habit by id"""
    habit = query_habit_by_id(habit_id)
    completions = query_completions_by_habit_id(habit_id)
    if not habit or not completions: 
        return 0

    max_streak = 0
    current_streak = 0
    prev_date = None
    gap = get_period_delta(habit["periodicity"])

    for c in completions:
        date = parse_date(c["completion_date"])
        if prev_date is None or (date - prev_date).days <= gap:
            current_streak += 1
        else:
            current_streak = 1
        prev_date = date
        max_streak = max(max_streak, current_streak)

    return max_streak


def get_streak_by_habit_id(habit_id: int) -> int:
    """"Get the current streaks of all habits"""
    habit = query_habit_by_id(habit_id)
    completions = query_completions_by_habit_id(habit_id, "DESC")

    if not habit or not completions: 
        return 0

    current_streak = 0
    prev_date = None
    gap = get_period_delta(habit["periodicity"])

    for c in completions:
        date = parse_date(c["completion_date"])
        if prev_date is None or (prev_date - date).days <= gap:
            current_streak += 1
        else:
            break
    prev_date = date

    return current_streak


def get_streaks() -> list[dict]:
    return [{"id": item['id'], "streak": get_streak_by_habit_id(item['id'])} for item in get_habits()]
