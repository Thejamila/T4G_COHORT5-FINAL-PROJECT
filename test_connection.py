from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(DATABASE_URL)

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ Successfully connected to MySQL!")
        print("Database: banking_db")

except Exception as e:
    print("❌ Connection failed.")
    print("Error:", e)
