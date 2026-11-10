import todo
import todo.commands


def test_main_returns_nonzero_exit_code_on_unknown_command(capsys):
    """Unknown commands must fail the process (non-zero exit code)."""
    assert todo.main(["no-such-command"]) == 1


def test_main_returns_nonzero_exit_code_on_deprecated_command(capsys):
    """Deprecated underscore aliases must fail the process (non-zero exit code)."""
    assert todo.main(["list_groups"]) == 1


def test_main_returns_zero_exit_code_on_success(monkeypatch):
    """A successfully run command must exit zero."""

    class FakeCommands:
        def __init__(self, command):
            pass

        def run(self, arguments):
            return None

    monkeypatch.setattr(todo.commands, "Commands", FakeCommands)
    assert todo.main(["list"]) == 0
