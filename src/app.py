from src.cli import cli
from src.infra.initialization import init_app

if __name__ == "__main__":
    init_app()
    cli()
