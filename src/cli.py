import click

from src.analytics import (
    get_habits,
    get_habits_by_period,
    get_longest_streak_by_id,
    get_streaks,
)
from src.habit_tracker import HabitTracker

tracker = HabitTracker()


@click.group()
def cli():
    """Habit Tracker CLI"""
    pass


# -------------------------
# CRUD Commands
# -------------------------


@cli.command()
@click.argument("name")
@click.option("--description", default="", help="Optional description")
@click.option(
    "--periodicity", type=click.Choice(["daily", "weekly", "biweekly"]), required=True
)
@click.option("--start-date", default="2025-01-01", help="Start date in YYYY-MM-DD")
def create(name, description, periodicity, start_date):
    """Create a new habit"""
    habit_id = tracker.create_habit(
        {
            "name": name,
            "description": description,
            "periodicity": periodicity,
            "start_date": start_date,
        }
    )
    click.echo(f"Habit created with ID {habit_id}")


@cli.command()
@click.argument("habit_id", type=int)
def delete(habit_id):
    """Delete a habit by ID"""
    result = tracker.delete_habit(habit_id)
    if result:
        click.echo("Habit deleted.")
    else:
        click.echo("Habit not found.")


@cli.command()
@click.argument("habit_id", type=int)
def complete(habit_id):
    """Complete a habit"""
    try:
        completion_id = tracker.complete_habit(habit_id)
        click.echo(f"Habit completed. Completion ID: {completion_id}")
    except ValueError as e:
        click.echo(f"Error: {e}")


# -------------------------
# Analytics Commands
# -------------------------


@cli.command()
@click.option(
    "--period", type=click.Choice(["daily", "weekly", "biweekly"]), required=True
)
def list_by_period(period):
    """List habits by periodicity"""
    habits = get_habits_by_period(period)
    for h in habits:
        click.echo(f"[{h['id']}] {h['name']} ({h['periodicity']})")


@cli.command()
def list_all():
    """List all habits"""
    for h in get_habits():
        click.echo(f"[{h['id']}] {h['name']} ({h['periodicity']})")


@cli.command()
@click.argument("habit_id", type=int)
def longest_streak(habit_id):
    """Get longest streak for a habit"""
    streak = get_longest_streak_by_id(habit_id)
    click.echo(f"Longest streak for habit {habit_id}: {streak}")


@cli.command()
def streaks():
    """Get current streaks for all habits"""
    for entry in get_streaks():
        click.echo(f"Habit {entry['id']} – Current Streak: {entry['streak']}")
