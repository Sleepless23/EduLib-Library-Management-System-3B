import os
import tempfile
import pytest
import sqlite3
from src import database

@pytest.fixture
def test_db(monkeypatch):
    # Create temporary db file
    fd, path = tempfile.mkstemp()
    os.close(fd)

    # Patch DB_FILE used inside database.py
    monkeypatch.setattr(database, "DB_FILE", path)

    # Initialize database structure
    database.initialize_db()

    yield path  # provide DB path to test

    os.remove(path)  # cleanup
