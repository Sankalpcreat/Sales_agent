import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
try:
    conn = psycopg2.connect(db_url)
    print("Database connection successful!")
    conn.close()
except Exception as e:
    print(f"Error connecting to database: {e}")
