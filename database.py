"""
Database connection setup.

This file's only job is: connect to MySQL, and hand out a "session"
(a temporary connection) to any part of the app that needs to
read or write data.

It reads your MySQL username, password, host, port, and database
name from a file called .env, so your real password is never
typed directly into this code or pushed to GitHub.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Reads the .env file and loads DB_USER, DB_PASSWORD, etc. into the environment
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

# This builds the full connection string SQLAlchemy uses to reach MySQL,
# e.g. mysql+pymysql://jamila:0108@localhost:3306/banking_db
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# The "engine" is the actual connection to MySQL.
# pool_pre_ping checks the connection is still alive before using it,
# which avoids random "MySQL server has gone away" errors.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal is a factory that creates a new "conversation" with the
# database each time it's called.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Used by every route that needs the database.
    Opens a session, hands it over, then closes it when the route is done -
    even if the route crashes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
