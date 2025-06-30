from src.modules.habit_tracker import HabitTracker
from src.modules.analytics import get_habits, get_habits_by_period, get_streaks
from src.db.database import init_db, seed_initial_habits
import datetime

habit = HabitTracker()


# Call this only once at program start
if __name__ == "__main__":
    today = datetime.date.today().isoformat()
    init_db()
    seed_initial_habits()
    habit.create_habit({"id": 100, "creation_date": today, "name": "test", "periodicity": "biweekly", "description": "testing"})
    print(get_habits())