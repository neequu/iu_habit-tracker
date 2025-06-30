from datetime import datetime
from src.model import Periodicity

parse_date = lambda s: datetime.strptime(s, "%Y-%m-%d").date()

def get_period_delta(p: Periodicity) -> int:
    return {
        "daily": 1,
        "weekly": 7,
        "biweekly": 14,
    }[p]
