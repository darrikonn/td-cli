import sqlite3
import pytest

from todo.services.group import GroupService
from todo.services.todo import TodoService


@pytest.fixture
def db_connection():
    """Create an in-memory SQLite database for testing."""
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Initialize tables
    group_service = GroupService(connection, cursor)
    todo_service = TodoService(connection, cursor)
    group_service.initialise_table()
    todo_service.initialise_table()
    
    connection.commit()
    yield connection, cursor
    
    connection.close()


@pytest.fixture
def group_service(db_connection):
    """Create a GroupService instance with test database."""
    connection, cursor = db_connection
    return GroupService(connection, cursor)


@pytest.fixture
def todo_service(db_connection):
    """Create a TodoService instance with test database."""
    connection, cursor = db_connection
    return TodoService(connection, cursor)


def test_edit_group_name_updates_todos(group_service, todo_service, db_connection):
    """Test that editing a group name updates all todos that reference it."""
    connection, cursor = db_connection
    
    # Create a group
    group_name = "testgroup"
    group_service.add(group_name)
    
    # Create todos in that group
    todo1_id = todo_service.add("Todo 1", "Details 1", group_name, False)
    todo2_id = todo_service.add("Todo 2", "Details 2", group_name, False)
    todo3_id = todo_service.add("Todo 3", "Details 3", None, False)  # No group
    
    # Verify todos are in the group
    cursor.execute("SELECT group_name FROM todo WHERE id = ?", (todo1_id,))
    assert cursor.fetchone()[0] == group_name
    
    cursor.execute("SELECT group_name FROM todo WHERE id = ?", (todo2_id,))
    assert cursor.fetchone()[0] == group_name
    
    cursor.execute("SELECT group_name FROM todo WHERE id = ?", (todo3_id,))
    assert cursor.fetchone()[0] is None
    
    # Edit the group name
    new_group_name = "renamedgroup"
    group_service.edit_name(new_group_name, group_name)
    
    # Verify the group name was updated
    cursor.execute("SELECT name FROM \"group\" WHERE name = ?", (new_group_name,))
    assert cursor.fetchone() is not None
    
    cursor.execute("SELECT name FROM \"group\" WHERE name = ?", (group_name,))
    assert cursor.fetchone() is None
    
    # Verify todos in the group were updated
    cursor.execute("SELECT group_name FROM todo WHERE id = ?", (todo1_id,))
    assert cursor.fetchone()[0] == new_group_name
    
    cursor.execute("SELECT group_name FROM todo WHERE id = ?", (todo2_id,))
    assert cursor.fetchone()[0] == new_group_name
    
    # Verify todo without group was not affected
    cursor.execute("SELECT group_name FROM todo WHERE id = ?", (todo3_id,))
    assert cursor.fetchone()[0] is None
