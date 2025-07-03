from click.testing import CliRunner

from src.cli import cli


def test_create_habit_minimal():
    """Should create a new habit with minimal valid input"""
    runner = CliRunner()
    result = runner.invoke(cli, ["create", "Yoga", "--periodicity", "daily"])
    assert result.exit_code == 0
    assert "created" in result.output.lower()


def test_create_habit_missing_periodicity():
    """Should fail when required option is missing"""
    runner = CliRunner()
    result = runner.invoke(cli, ["create", "Yoga"])
    assert result.exit_code != 0
    assert "missing option '--periodicity'" in result.output.lower()


def test_create_habit_invalid_periodicity():
    """Should reject invalid periodicity value"""
    runner = CliRunner()
    result = runner.invoke(cli, ["create", "Sleep", "--periodicity", "yearly"])
    assert result.exit_code != 0
    assert "invalid value for '--periodicity'" in result.output.lower()


def test_list_habits_shows_created():
    """Should display habit in list after creation"""
    runner = CliRunner()
    runner.invoke(cli, ["create", "Meditation", "--periodicity", "weekly"])
    result = runner.invoke(cli, ["list"])
    assert "meditation" in result.output.lower()


def test_complete_habit_requires_valid_id():
    """Should mark habit complete and reject invalid ID"""
    runner = CliRunner()

    # Create habit
    create_result = runner.invoke(cli, ["create", "Running", "--periodicity", "daily"])
    habit_id = int(create_result.output.strip().split()[-1])

    # Complete habit
    complete_result = runner.invoke(cli, ["complete", str(habit_id)])
    assert complete_result.exit_code == 0
    assert "completed" in complete_result.output.lower()

    # Try completing non-existent habit
    bad_result = runner.invoke(cli, ["complete", "99999"])
    assert bad_result.exit_code != 0
    assert "not found" in bad_result.output.lower()


def test_delete_habit_removes_it():
    """Should delete habit and confirm it’s gone"""
    runner = CliRunner()
    create_result = runner.invoke(
        cli, ["create", "Sleep Early", "--periodicity", "daily"]
    )
    habit_id = int(create_result.output.strip().split()[-1])

    delete_result = runner.invoke(cli, ["delete", str(habit_id)])
    assert delete_result.exit_code == 0
    assert "deleted" in delete_result.output.lower()

    list_result = runner.invoke(cli, ["list"])
    assert "sleep early" not in list_result.output.lower()


def test_delete_habit_invalid_id():
    """Should fail gracefully if ID doesn't exist"""
    runner = CliRunner()
    result = runner.invoke(cli, ["delete", "99999"])
    assert result.exit_code != 0
    assert "not found" in result.output.lower()
