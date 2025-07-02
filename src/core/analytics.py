import datetime

from src.infra.database import (
    query_completions_by_habit_id,
    query_habit_by_id,
    query_habits,
    query_habits_by_period,
)
from src.infra.date_utils import get_period_delta, parse_date

from .model import HabitType, Periodicity


def get_habits_by_period(period: Periodicity) -> list[HabitType]:
    """Get habits by period."""
    return query_habits_by_period(period)


def get_habits() -> list[HabitType]:
    """ "Get all habits"""
    return query_habits()


def get_longest_streak_by_id(habit_id: int) -> int:
    """Get the longest streak of a single habit by id"""
    habit = query_habit_by_id(habit_id)
    completions = query_completions_by_habit_id(habit_id)
    if not habit or not completions:
        return 0

    max_streak = 1
    current_streak = 1
    gap = get_period_delta(habit["periodicity"])

    for i in range(1, len(completions)):
        prev_date = parse_date(completions[i - 1]["completion_date"])
        curr_date = parse_date(completions[i]["completion_date"])

        if (curr_date - prev_date).days <= gap:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1

    return max_streak


def get_streak_by_habit_id(habit_id: int) -> int:
    habit = query_habit_by_id(habit_id)
    completions = query_completions_by_habit_id(habit_id, "DESC")

    if not habit or not completions:
        return 0

    gap = get_period_delta(habit["periodicity"])

    latest_date = parse_date(completions[0]["completion_date"])
    if (datetime.date.today() - latest_date).days > gap:
        return 0

    current_streak = 1
    prev_date = latest_date

    for c in completions[1:]:
        date = parse_date(c["completion_date"])
        if (prev_date - date).days <= gap:
            current_streak += 1
            prev_date = date
        else:
            break

    return current_streak


def get_streaks() -> list[dict]:
    return [
        {"id": item["id"], "streak": get_streak_by_habit_id(item["id"])}
        for item in get_habits()
    ]
