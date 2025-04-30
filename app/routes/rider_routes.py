from fastapi import APIRouter, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from app.database.db import get_db_connection
from app.models.rider import RiderCreate, RiderResponse, RiderStatusUpdate
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/register", response_model=RiderResponse)
def register_rider(rider: RiderCreate, current_user: dict = Depends(get_current_user)):
    """Registers a new rider"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute(
            "INSERT INTO riders (user_id, vehicle_type, license_plate, status) VALUES (%s, %s, %s, 'Available') RETURNING id, user_id, vehicle_type, license_plate, status",
            (rider.user_id, rider.vehicle_type, rider.license_plate),
        )

        new_rider = cursor.fetchone()
        conn.commit()

        return RiderResponse(**new_rider)

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cursor.close()
        conn.close()

@router.get("/{rider_id}", response_model=RiderResponse)
def get_rider(rider_id: int):
    """Retrieves a rider's details"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM riders WHERE id = %s", (rider_id,))
    rider = cursor.fetchone()

    cursor.close()
    conn.close()

    if not rider:
        raise HTTPException(status_code=404, detail="Rider not found")

    return RiderResponse(**rider)

@router.patch("/{rider_id}/status", response_model=RiderResponse)
def update_rider_status(rider_id: int, status_update: RiderStatusUpdate):
    """Updates rider status (Available/Busy)"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("UPDATE riders SET status = %s WHERE id = %s RETURNING *", (status_update.status, rider_id))
        updated_rider = cursor.fetchone()
        conn.commit()

        if not updated_rider:
            raise HTTPException(status_code=404, detail="Rider not found")

        return RiderResponse(**updated_rider)

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cursor.close()
        conn.close()
