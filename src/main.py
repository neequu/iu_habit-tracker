from src.database import init_db, seed_initial_habits
from src.habit_tracker import HabitTracker
import datetime



habit = HabitTracker()

today = datetime.date.today().isoformat()

# predefined habits (at least 1 daily, 1 weekly)
habits = [
    ("Drink Water", "Stay hydrated by drinking 8 glasses", "daily", today),
    ("Exercise", "Do 20 minutes of physical activity", "daily", today),
    ("Read Book", "Read 10 pages of a book", "daily", today),
    ("Call Parents", "Weekly call to family", "weekly", today),
    ("Clean Room", "Tidy and organize living space", "weekly", today),
]


# call this only once at program start
if __name__ == "__main__":
    init_db()
    seed_initial_habits(habits)
    habit.create_habit({"start_date": today, "name": "test", "periodicity": "biweekly", "description": "testing"})