from src.database import init_db, seed_initial_habits
from src.habit_tracker import HabitTracker
import datetime
from src.constants import today, initial_habits


# call this only once at program start
if __name__ == "__main__":
    init_db()
    seed_initial_habits(initial_habits)
    habit = HabitTracker()