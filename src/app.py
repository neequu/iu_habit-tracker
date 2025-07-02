from src.cli import cli
from src.core.constants import initial_habits
from src.infra.database import init_db, seed_initial_habits

# call this only once at program start
if __name__ == "__main__":
    init_db()
    seed_initial_habits(initial_habits)
    cli()
