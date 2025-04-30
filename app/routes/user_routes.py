from fastapi import APIRouter, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from app.database.db import get_db_connection
from app.models.user import UserCreate, UserLogin, UserResponse
from app.utils.auth import hash_password, verify_password, create_jwt_token, get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate):
    """Registers a new user"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        hashed_password = hash_password(user.password)
        cursor.execute(
            "INSERT INTO users (name, phone_number, password, is_admin) VALUES (%s, %s, %s, %s) RETURNING id, name, phone_number, is_admin",
            (user.name, user.phone_number, hashed_password, user.is_admin),
        )
        new_user = cursor.fetchone()
        conn.commit()

        return UserResponse(**new_user)

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cursor.close()
        conn.close()

@router.post("/login")
def login_user(user: UserLogin):
    """User login & JWT token generation"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("SELECT id, name, phone_number, password, is_admin FROM users WHERE phone_number = %s", (user.phone_number,))
        existing_user = cursor.fetchone()

        if not existing_user or not verify_password(user.password, existing_user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_jwt_token({"user_id": existing_user["id"], "phone_number": existing_user["phone_number"], "is_admin": existing_user["is_admin"]})

        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cursor.close()
        conn.close()

@router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    """Protected route to test JWT authentication"""
    return {"message": f"Hello, {current_user['phone_number']}! You are authorized."}
