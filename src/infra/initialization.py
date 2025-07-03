from src.core.constants import initial_habits
from src.infra.database import init_db, seed_initial_habits


def init_app() -> None:
    init_db()
    seed_initial_habits(initial_habits)
