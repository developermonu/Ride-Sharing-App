import psycopg2
from psycopg2 import sql
from app.database.db import get_db_connection
from app.utils.auth import hash_password

def create_tables():
    conn = get_db_connection()
    if not conn:
        print("❌ Database connection failed!")
        return

    cursor = conn.cursor()
    table_creation_queries = [
        sql.SQL("""
            CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone_number VARCHAR(20) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE  -- Add this column
        );

        """),
        sql.SQL("""
            CREATE TABLE IF NOT EXISTS riders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                vehicle_type VARCHAR(50) NOT NULL,
                license_plate VARCHAR(20) UNIQUE NOT NULL,
                status VARCHAR(20) DEFAULT 'Available'
            );
        """),
        sql.SQL("""
            CREATE TABLE IF NOT EXISTS bookings (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                rider_id INTEGER REFERENCES riders(id) ON DELETE SET NULL,
                status VARCHAR(20) DEFAULT 'Pending',
                distance INTEGER NOT NULL,
                fare INTEGER NOT NULL
            );
        """)
    ]

    try:
        for query in table_creation_queries:
            cursor.execute(query)

        conn.commit()
        print("✅ Database tables created successfully!")

        seed_database(cursor, conn)

    except Exception as e:
        print(f"❌ Error creating tables: {e}")

    finally:
        cursor.close()
        conn.close()

def seed_database(cursor, conn):
    sample_users = [
        ("Nguyen Van A", "1111111111", hash_password("password123")),
        ("Tran Thi B", "2222222222", hash_password("password123")),
        ("Le Van C", "3333333333", hash_password("password123")),
        ("Pham Thi D", "4444444444", hash_password("password123")),
        ("Hoang Van E", "5555555555", hash_password("password123"))
    ]

    sample_riders = [
        (1, "Swift", "59A1-12345"),
        (2, "Mercedes", "59B1-67890"),
        (3, "BMW", "51C-11223"),
        (4, "Lord Alto", "51D-44556"),
        (5, "Kawasaki Ninja", "51E-77889")
    ]

    try:
        for name, phone_number, password in sample_users:
            cursor.execute(
                "INSERT INTO users (name, phone_number, password) VALUES (%s, %s, %s) ON CONFLICT (phone_number) DO NOTHING",
                (name, phone_number, password),
            )

        for user_id, vehicle_type, license_plate in sample_riders:
            cursor.execute(
                "INSERT INTO riders (user_id, vehicle_type, license_plate) VALUES (%s, %s, %s) ON CONFLICT (license_plate) DO NOTHING",
                (user_id, vehicle_type, license_plate),
            )

        conn.commit()
        print("✅ Database seeded with sample users and riders!")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error seeding database: {e}")
