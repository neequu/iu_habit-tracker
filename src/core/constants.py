from datetime import date


def get_today_date_string() -> str:
    return date.today().isoformat()


# predefined habits (at least 1 daily, 1 weekly)
initial_habits = [
    (
        "Drink Water",
        "Stay hydrated by drinking 8 glasses",
        "daily",
        get_today_date_string(),
    ),
    (
        "Exercise",
        "Do 20 minutes of physical activity",
        "daily",
        get_today_date_string(),
    ),
    ("Read Book", "Read 10 pages of a book", "daily", get_today_date_string()),
    ("Call Parents", "Weekly call family", "weekly", get_today_date_string()),
    ("Clean Room", "Tidy and organize living space", "weekly", get_today_date_string()),
]


PERIOD_DELTAS = {
    "daily": 1,
    "weekly": 7,
    "biweekly": 14,
}
