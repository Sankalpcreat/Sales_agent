import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def connect_to_database():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Database connection successful!")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def verify_connection():
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                print("Database query executed successfully!")
        except Exception as e:
            print(f"Database query failed: {e}")
        finally:
            conn.close()

