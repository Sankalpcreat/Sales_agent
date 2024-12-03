import pytest
import psycopg2
from core.database import connect_to_database, verify_connection, execute_query


@pytest.fixture
def mock_env_variables(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:password@localhost:5432/test_db")


@pytest.fixture
def mock_psycopg2_connect(mocker):
    # Create mock cursor and connection
    mock_cursor = mocker.Mock()
    mock_conn = mocker.Mock()
    
    # Setup cursor context manager
    mock_cursor_cm = mocker.Mock()
    mock_cursor_cm.__enter__ = mocker.Mock(return_value=mock_cursor)
    mock_cursor_cm.__exit__ = mocker.Mock(return_value=None)
    
    # Setup connection to return cursor context manager
    mock_conn.cursor.return_value = mock_cursor_cm
    
    # Patch psycopg2.connect
    mocker.patch("core.database.psycopg2.connect", return_value=mock_conn)
    return mock_conn, mock_cursor


def test_connect_to_database_success(mock_env_variables, mock_psycopg2_connect):
    mock_conn, _ = mock_psycopg2_connect
    conn = connect_to_database()
    assert conn == mock_conn
    mock_conn.cursor.assert_not_called()


def test_connect_to_database_failure(mock_env_variables, mocker):
    mocker.patch("core.database.psycopg2.connect", side_effect=Exception("Connection error"))
    conn = connect_to_database()
    assert conn is None


def test_verify_connection_success(mock_env_variables, mock_psycopg2_connect):
    mock_conn, mock_cursor = mock_psycopg2_connect
    verify_connection()
    mock_cursor.execute.assert_called_once_with("SELECT 1;")
    mock_conn.close.assert_called_once()


def test_verify_connection_failure(mock_env_variables, mocker):
    # Create mocks
    mock_cursor = mocker.Mock()
    mock_cursor.execute.side_effect = Exception("Query error")
    
    mock_cursor_cm = mocker.Mock()
    mock_cursor_cm.__enter__ = mocker.Mock(return_value=mock_cursor)
    mock_cursor_cm.__exit__ = mocker.Mock(return_value=None)
    
    mock_conn = mocker.Mock()
    mock_conn.cursor.return_value = mock_cursor_cm
    
    mocker.patch("core.database.psycopg2.connect", return_value=mock_conn)
    
    verify_connection()
    mock_cursor.execute.assert_called_once_with("SELECT 1;")
    mock_conn.close.assert_called_once()


def test_execute_query_success(mock_env_variables, mock_psycopg2_connect):
    mock_conn, mock_cursor = mock_psycopg2_connect
    mock_cursor.fetchall.return_value = [(1, "test")]
    
    result = execute_query("SELECT * FROM test")
    assert result == [(1, "test")]
    mock_cursor.execute.assert_called_once_with("SELECT * FROM test", None)
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_execute_query_failure(mock_env_variables, mocker):
    # Create mocks
    mock_cursor = mocker.Mock()
    mock_cursor.execute.side_effect = Exception("Execution error")
    
    mock_cursor_cm = mocker.Mock()
    mock_cursor_cm.__enter__ = mocker.Mock(return_value=mock_cursor)
    mock_cursor_cm.__exit__ = mocker.Mock(return_value=None)
    
    mock_conn = mocker.Mock()
    mock_conn.cursor.return_value = mock_cursor_cm
    
    mocker.patch("core.database.psycopg2.connect", return_value=mock_conn)
    
    result = execute_query("SELECT * FROM test")
    assert result is None
    mock_cursor.execute.assert_called_once_with("SELECT * FROM test", None)
    mock_conn.close.assert_called_once()