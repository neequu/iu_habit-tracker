from src.constants import initial_habits, today
from src.database import init_db, seed_initial_habits
from src.habit_tracker import HabitTracker

# call this only once at program start
if __name__ == "__main__":
    init_db()
    seed_initial_habits(initial_habits)
    habit = HabitTracker()
