import pytest
import psycopg2
from core.database import connect_to_database, verify_connection, execute_query


@pytest.fixture
def mock_env_variables(monkeypatch):
    
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:password@localhost:5432/test_db")


@pytest.fixture
def mock_psycopg2_connect(mocker):
    
    mock_conn = mocker.Mock()
    mock_conn.cursor.return_value.__enter__.return_value = mocker.Mock()
    mocker.patch("core.database.psycopg2.connect", return_value=mock_conn)
    return mock_conn


def test_connect_to_database_success(mock_env_variables, mock_psycopg2_connect):
    
    conn = connect_to_database()
    assert conn == mock_psycopg2_connect
    mock_psycopg2_connect.cursor.assert_not_called()


def test_connect_to_database_failure(mock_env_variables, mocker):
    
    mocker.patch("core.database.psycopg2.connect", side_effect=Exception("Connection error"))
    conn = connect_to_database()
    assert conn is None


def test_verify_connection_success(mock_env_variables, mock_psycopg2_connect):
    
    verify_connection()
    mock_psycopg2_connect.cursor.return_value.__enter__.return_value.execute.assert_called_once_with("SELECT 1;")


def test_verify_connection_failure(mock_env_variables, mocker):
    
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.execute.side_effect = Exception("Query error")
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mocker.patch("core.database.psycopg2.connect", return_value=mock_conn)

    verify_connection()
    mock_cursor.execute.assert_called_once_with("SELECT 1;")


def test_execute_query_success(mock_env_variables, mock_psycopg2_connect):
    
    mock_cursor = mock_psycopg2_connect.cursor.return_value.__enter__.return_value
    mock_cursor.fetchall.return_value = [("result",)]
    query = "SELECT * FROM test_table"
    params = None

    result = execute_query(query, params)
    assert result == [("result",)]
    mock_cursor.execute.assert_called_once_with(query, params)


def test_execute_query_failure(mock_env_variables, mocker):
    
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.execute.side_effect = Exception("Execution error")
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mocker.patch("core.database.psycopg2.connect", return_value=mock_conn)

    query = "SELECT * FROM test_table"
    params = None
    result = execute_query(query, params)
    assert result is None
    mock_cursor.execute.assert_called_once_with(query, params)