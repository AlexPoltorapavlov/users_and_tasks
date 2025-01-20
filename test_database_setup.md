# Test Database Setup Guide

The test database is already configured to be created at the beginning of testing and deleted at the end of testing using pytest fixtures in `test/conftest.py`. Here's how it works:

1. The `db_file` fixture (lines 81-94):
   - Creates a temporary SQLite database file named "test_database.db"
   - Uses pytest's `yield` mechanism to provide the database path during tests
   - After all tests complete, it automatically deletes the database file if it exists

2. The `create_db_and_tables` fixture (lines 114-126):
   - Takes the SQLAlchemy engine as input
   - Creates all database tables defined in your models
   - Runs automatically before tests that depend on it

3. The `test_db` fixture (line 156):
   - Combines both database creation and session management
   - Ensures database tables are created before tests run
   - Will be cleaned up after tests complete

To use this in your tests, simply add the `test_db` fixture as a parameter to your test functions:

```python
async def test_something(test_db):
    # Your test code here
    pass
```

The database will be:
- Created fresh at the start of testing
- Available during all tests
- Automatically deleted when testing completes