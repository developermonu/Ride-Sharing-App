from fastapi import APIRouter, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from app.database.db import get_db_connection
from app.utils.auth import get_current_user
from app.models.admin import UserResponse, RiderResponse, RideResponse
from app.models.user import UserCreate, UserUpdate

router = APIRouter()

def admin_required(current_user: dict = Depends(get_current_user)):
    if not current_user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.get("/dashboard")
def admin_dashboard(current_user: dict = Depends(admin_required)):
    """Admin dashboard (Protected)"""
    return {"message": "Welcome to Admin Dashboard!"}

@router.get("/users", response_model=list[UserResponse])
def get_users(current_user: dict = Depends(admin_required)):
    """Get all users"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users

@router.get("/riders", response_model=list[RiderResponse])
def get_riders(current_user: dict = Depends(admin_required)):
    """Get all riders"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM riders")
    riders = cursor.fetchall()

    cursor.close()
    conn.close()

    return riders

@router.get("/rides", response_model=list[RideResponse])
def get_rides(current_user: dict = Depends(admin_required)):
    """Get all rides"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM bookings")
    rides = cursor.fetchall()

    cursor.close()
    conn.close()

    return rides

@router.patch("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, current_user: dict = Depends(admin_required)):
    """Update user details"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute(
            """
            UPDATE users SET name = %s, phone_number = %s, is_admin = %s
            WHERE id = %s RETURNING id, name, phone_number, is_admin
            """,
            (user.name, user.phone_number, user.is_admin, user_id),
        )
        updated_user = cursor.fetchone()
        conn.commit()

        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")

        return UserResponse(**updated_user)

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cursor.close()
        conn.close()
