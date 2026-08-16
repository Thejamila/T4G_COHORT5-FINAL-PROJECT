"""
This is the starting point of the whole app - the file uvicorn runs
when you type: uvicorn main:app --reload

All it does is:
1. Connect to the database and make sure the tables exist.
2. Create the FastAPI app.
3. Plug in every route from routes/.
"""

from fastapi import FastAPI

from database import engine
from models.base_models import Base
from routes import api_router

# This line creates the customers and accounts tables in MySQL
# automatically, the first time the app runs - you never have to
# write CREATE TABLE yourself.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Banking System API",
    description="A REST API for managing customers and their bank/savings accounts.",
    version="1.0.0",
)

app.include_router(api_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Banking System API is running. Visit /docs for the interactive docs."
    }
