import datetime

today = datetime.date.today().isoformat()

# predefined habits (at least 1 daily, 1 weekly)
initial_habits = [
    ("Drink Water", "Stay hydrated by drinking 8 glasses", "daily", today),
    ("Exercise", "Do 20 minutes of physical activity", "daily", today),
    ("Read Book", "Read 10 pages of a book", "daily", today),
    ("Call Parents", "Weekly call to family", "weekly", today),
    ("Clean Room", "Tidy and organize living space", "weekly", today),
]


PERIOD_DELTAS = {
    "daily": 1,
    "weekly": 7,
    "biweekly": 14,
}
