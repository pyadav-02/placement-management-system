import sqlite3
import pytest
from unittest.mock import MagicMock
from database_utility.database_sqlite3_utils import OpenDatabase


class TestOpenDatabase:
    def setup_method(self):
        self.db = OpenDatabase('abc')

    def test_connect(self, monkeypatch):
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect = MagicMock(return_value=mock_connection)

        monkeypatch.setattr('sqlite3.connect', mock_connect)

        result = self.db.connect()
        assert result == mock_cursor
        mock_connect.assert_called_once_with('abc')
        mock_connection.cursor.assert_called_once()

