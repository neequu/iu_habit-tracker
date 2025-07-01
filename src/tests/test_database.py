

from src.database import (
    add_habit,
    query_habit_by_id,
    delete_habit_by_id,
    add_completion,
    query_completions_by_habit_id,
    query_habits,
    query_habits_by_period,
    query_latest_completion_by_habit_id,
)

from src.model import CreateHabitBody

def test_add_and_retrieve_habits() -> None:
    """Test that habits can be added and retrieved"""
    # Initial data
    habit_name = "test habit"
    habit_periodicity = 'daily'

    habit_data: CreateHabitBody = {
        "name": habit_name,
        "description": "test description",
        "periodicity": habit_periodicity,
        "start_date": "2025-01-01"
    }
    
    # Get initial habits
    habits = query_habits()

    # Check if added was added
    habit_id = add_habit(habit_data)
    assert habit_id is not None, "Habit creation failed"
    habit = query_habit_by_id(habit_id)
    assert habit is not None, "Habit query failed"
    assert habit["name"] == habit_name
    assert habit["periodicity"] == habit_periodicity
    # Check if single habit was added
    updated_habits = query_habits()
    assert len(updated_habits) - len(habits) == 1, "Habit was not added to DB"


def test_add_and_delete_habit():
    """Test that habits can be deleted"""
    # Initial data
    habit_data: CreateHabitBody = {
        "name": "for deletion",
        "description": "will be deleted",
        "periodicity": "weekly",
        "start_date": "2025-05-05"
    }
    
    # Check if habit was added
    habit_id = add_habit(habit_data)
    assert habit_id is not None, "Habit creation failed"

    # Check if habit was deleted
    success = delete_habit_by_id(habit_id)
    assert success == True, "Habit was not deleted"
    habit = query_habit_by_id(habit_id)
    assert habit is None, "Habit was not removed from DB"



def test_query_habits_by_period():
    # Initial habit data
    habit_data: list[CreateHabitBody] = [
      {
          "name": "Daily Exercise",
          "description": "30 minutes of cardio",
          "periodicity": "daily",
          "start_date": "2025-01-02"
      },
      {
          "name": "Weekly Review",
          "description": "Work tasks review",
          "periodicity": "weekly",
          "start_date": "2025-01-01"
      }
  ]
    # Initial period data
    initial_daily_habits = query_habits_by_period("daily")
    initial_weekly_habits = query_habits_by_period("weekly")
    initial_biweekly_habits = query_habits_by_period("biweekly")

    # Request body creation
    habit_ids = []
    for habit in habit_data:
        habit_id = add_habit(habit)
        assert habit_id is not None
        habit_ids.append(habit_id)


    # Test daily habits
    daily_habits = query_habits_by_period("daily")
    assert len(daily_habits) - len(initial_daily_habits) == 1, "Wrong habit daily period added"

    # Test weekly habits
    weekly_habits = query_habits_by_period("weekly")
    assert len(weekly_habits) - len(initial_weekly_habits) == 1, "Wrong habit weekly period added"

    # Test empty case
    biweekly_habits = query_habits_by_period("biweekly")
    assert len(biweekly_habits) - len(initial_biweekly_habits) == 0, "Wrong habit biweekly period added"


def test_add_and_retrieve_completion() -> None:
    """Test that completions can be added and retrieved"""
    # Arrange
    habit_data: CreateHabitBody = {
        "name": "Test Habit",
        "description": "Test Description",
        "periodicity": "daily",
        "start_date": "2025-10-10"
    }
    completion_date = "2025-10-17"
    
    # Create habit
    habit_id = add_habit(habit_data)
    assert habit_id is not None, "Habit creation failed"
    
    # Verify initial state
    initial_completions = query_completions_by_habit_id(habit_id)
    assert len(initial_completions) == 0, "Should start with no completions"
    
    # Add completion
    completion_id = add_completion({
        "habit_id": habit_id, 
        "completion_date": completion_date
    })
    assert completion_id is not None, "Completion creation failed"
    
    # Verify changes
    updated_completions = query_completions_by_habit_id(habit_id)
    assert len(updated_completions) == 1, "Should have exactly one completion"
    
    latest_completion = query_latest_completion_by_habit_id(habit_id)
    assert latest_completion is not None, "Should find latest completion"
    assert latest_completion['completion_date'] == completion_date
    assert latest_completion['habit_id'] == habit_id