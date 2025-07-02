import datetime

from src.core.analytics import (
    get_habits_by_period,
    get_longest_streak_by_id,
    get_streak_by_habit_id,
    get_streaks,
)
from src.core.model import CreateHabitBody
from src.infra.database import add_completion, add_habit


def test_get_habits_by_period(habit_factory):
    # Initial habit data
    habit_data: list[CreateHabitBody] = [
        habit_factory(periodicity="daily"),
        habit_factory(periodicity="weekly"),
    ]
    # Initial period data
    initial_daily_habits = get_habits_by_period("daily")
    initial_weekly_habits = get_habits_by_period("weekly")
    initial_biweekly_habits = get_habits_by_period("biweekly")

    # Request body creation
    habit_ids = []
    for habit in habit_data:
        habit_id = add_habit(habit)
        assert habit_id is not None
        habit_ids.append(habit_id)

    # Test daily habits
    daily_habits = get_habits_by_period("daily")
    assert (
        len(daily_habits) - len(initial_daily_habits) == 1
    ), "Wrong habit daily period added"

    # Test weekly habits
    weekly_habits = get_habits_by_period("weekly")
    assert (
        len(weekly_habits) - len(initial_weekly_habits) == 1
    ), "Wrong habit weekly period added"

    # Test empty case
    biweekly_habits = get_habits_by_period("biweekly")
    assert (
        len(biweekly_habits) - len(initial_biweekly_habits) == 0
    ), "Wrong habit biweekly period added"


def test_get_longest_streak_by_id(habit_factory):
    # Create a daily habit
    habit_id = add_habit(habit_factory())

    assert habit_id is not None

    # Add completions: a 3-day streak, 1-day break, then 2-day streak
    completions = [
        "2025-01-01",
        "2025-01-02",
        "2025-01-03",
        "2025-01-05",  # break on 2025-01-04
        "2025-01-06",
        "2025-01-07",
    ]

    for date in completions:
        add_completion({"habit_id": habit_id, "completion_date": date})

    longest = get_longest_streak_by_id(habit_id)
    assert longest == 3, f"Expected longest streak to be 3, got {longest}"


def test_get_streak_by_habit_id(habit_factory):
    # Create a daily habit
    habit_id = add_habit(habit_factory())
    assert habit_id is not None, "Failed to create habit"

    # Add completions leading up to yesterday (so current streak should be valid)
    today = datetime.date.today()
    completions = [
        (today - datetime.timedelta(days=2)).isoformat(),
        (today - datetime.timedelta(days=1)).isoformat(),
    ]

    for date in completions:
        add_completion({"habit_id": habit_id, "completion_date": date})

    streak = get_streak_by_habit_id(habit_id)
    assert streak == 2, f"Expected current streak to be 2, got {streak}"

    # Break the streak: completion too far back
    habit_id2 = add_habit(
        {"name": "Broken Streak", "periodicity": "daily", "start_date": "2025-01-01"}
    )
    assert habit_id2 is not None, "Failed to create habit"

    add_completion({"habit_id": habit_id2, "completion_date": "2024-12-01"})

    streak2 = get_streak_by_habit_id(habit_id2)
    assert streak2 == 0, f"Expected current streak to be 0, got {streak2}"


def test_get_streaks(habit_factory):
    # Create a few habits with various completion patterns
    habit_id = add_habit(habit_factory(name="Habit A"))
    assert habit_id is not None, "Failed to create habit"

    habit_id2 = add_habit(habit_factory(name="Habit B"))
    assert habit_id2 is not None, "Failed to create habit"

    today = datetime.date.today()
    add_completion(
        {
            "habit_id": habit_id,
            "completion_date": (today - datetime.timedelta(days=1)).isoformat(),
        }
    )
    add_completion(
        {
            "habit_id": habit_id,
            "completion_date": (today - datetime.timedelta(days=2)).isoformat(),
        }
    )

    add_completion(
        {"habit_id": habit_id2, "completion_date": "2024-01-01"}
    )  # too far back

    streaks = get_streaks()

    # We expect habit_id to have a current streak of 2, habit_id2 = 0
    streak_map = {item["id"]: item["streak"] for item in streaks}
    assert (
        streak_map[habit_id] == 2
    ), f"Habit A should have streak 2, got {streak_map[habit_id]}"
    assert (
        streak_map[habit_id2] == 0
    ), f"Habit B should have streak 0, got {streak_map[habit_id2]}"
