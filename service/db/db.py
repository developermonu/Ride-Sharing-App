import psycopg2
from app.database.config import DATABASE_CONFIG

def get_db_connection():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return None
