from models import HabitType, Periodicity
from utils import get_period_delta, parse_date

def get_habits_by_period(period: Periodicity) -> list[HabitType]:
  """Get habits by period."""
  habits = []
  return [item for item in habits if item.get("periodicity") == period]

def get_habits() -> list[HabitType]:
  """"Get all habits"""
  habits = []
  return habits.copy()

def get_longest_streak_by_id(habit_id: int) -> int:
    habits = []
    completions = []
    """"Get the longest streak of a single habit by id"""
    habit = next(h for h in habits if h["id"] == habit_id)
    relevant = [c for c in completions if c["habit_id"] == habit_id]
    relevant.sort(key=lambda x: x["completion_date"])

    max_streak = 0
    current_streak = 0
    prev_date = None
    gap = get_period_delta(habit["periodicity"])

    for c in relevant:
        date = parse_date(c["completion_date"])
        if prev_date is None or (date - prev_date).days <= gap:
            current_streak += 1
        else:
            current_streak = 1
        prev_date = date
        max_streak = max(max_streak, current_streak)

    return max_streak


def get_streak_by_habit_id(habit_id: int) -> int:
    habits = []
    completions = []
    """"Get the current streaks of all habits"""
    habit = next(h for h in habits if h["id"] == habit_id)
    relevant = [c for c in completions if c["habit_id"] == habit_id]
    relevant.sort(key=lambda x: x["completion_date"], reverse=True)

    current_streak = 0
    prev_date = None
    gap = get_period_delta(habit["periodicity"])

    for c in relevant:
        date = parse_date(c["completion_date"])
        if prev_date is None or (prev_date - date).days <= gap:
            current_streak += 1
        else:
            break
    prev_date = date

    return current_streak


def get_streaks() -> list[dict]:
    habits = []
    return [{"id": item['id'], "streak": get_streak_by_habit_id(item['id'])} for item in habits]
