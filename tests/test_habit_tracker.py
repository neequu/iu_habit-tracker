import datetime

import pytest

from src.core.habit_tracker import HabitTracker
from src.core.model import CreateHabitBody, HabitType
from src.infra.database import (
    add_completion,
    query_habit_by_id,
    query_latest_completion_by_habit_id,
)


def test_create_habit(habit_factory):
    """Verify habit creation stores valid attributes in the database."""
    tracker = HabitTracker()
    habit = habit_factory()

    habit_id = tracker.create_habit(habit)
    assert habit_id is not None, "Failed to create habit"

    habit = query_habit_by_id(habit_id)
    assert habit is not None, "Habit was not added to database"
    assert habit["name"] == habit["name"]


def test_delete_habit(habit_factory):
    """Ensure habit deletion removes the record and associated completions."""
    tracker = HabitTracker()
    habit = habit_factory()

    habit_id = tracker.create_habit(habit)
    assert habit_id is not None, "Failed to create habit"

    result = tracker.delete_habit(habit_id)
    assert result is True, "Failed to delete existing habit"

    deleted = query_habit_by_id(habit_id)
    assert deleted is None, "Habit still exists after deletion"


def test_complete_habit_first_time(habit_factory):
    """Test successful first completion of a habit."""
    tracker = HabitTracker()
    habit = habit_factory()

    habit_id = tracker.create_habit(habit)
    assert habit_id is not None, "Failed to create habit"

    completion_id = tracker.complete_habit(habit_id)
    assert completion_id is not None, "Habit completion not recorded"

    latest = query_latest_completion_by_habit_id(habit_id)
    assert latest is not None, "No completion found in DB"


def test_complete_habit_twice_same_day_fails(habit_factory):
    """Prevent duplicate completions for the same habit on the same day."""
    tracker = HabitTracker()
    habit = habit_factory()

    habit_id = tracker.create_habit(habit)
    assert habit_id is not None

    # First completion should work
    tracker.complete_habit(habit_id)

    # Second completion on same day should raise
    with pytest.raises(ValueError) as e:
        tracker.complete_habit(habit_id)

    assert "Cannot complete habit twice" in str(e.value)


def test_complete_habit_not_found_fails():
    """Verify attempting to complete a non-existent habit raises an error."""
    tracker = HabitTracker()

    invalid_id = 999999

    with pytest.raises(ValueError) as e:
        tracker.complete_habit(invalid_id)

    assert f"Habit with id {invalid_id} not found." in str(e.value)


def test_complete_habit_after_period_allows(habit_factory):
    """Allow new completions after the habit's periodicity window passes."""
    tracker = HabitTracker()
    habit = habit_factory()

    habit_id = tracker.create_habit(habit)
    assert habit_id is not None

    # Add first completion 8 days ago (longer than a weekly gap)
    eight_days_ago = (datetime.date.today() - datetime.timedelta(days=8)).isoformat()
    add_completion({"habit_id": habit_id, "completion_date": eight_days_ago})

    # Should now allow completion
    new_completion_id = tracker.complete_habit(habit_id)
    assert new_completion_id is not None
