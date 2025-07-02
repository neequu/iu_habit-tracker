from datetime import datetime

from src.core.constants import PERIOD_DELTAS
from src.core.model import Periodicity

parse_date = lambda s: datetime.strptime(s, "%Y-%m-%d").date()


def get_period_delta(p: Periodicity) -> int:
    return PERIOD_DELTAS[p]
