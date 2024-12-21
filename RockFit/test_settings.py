from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

"""
Database configuration for Django using an in-memory SQLite database.

The database is created in memory and will not persist after the testing session ends.

Settings:
- ENGINE: Specifies the backend to use. 
  'django.db.backends.sqlite3' for SQLite.
- NAME: The name of the database. ':memory:' so that the database 
  will be created in RAM and not saved to disk.

Usage:
This configuration is used in test settings to ensure that each 
test starts with a clean state, providing faster test execution.
"""