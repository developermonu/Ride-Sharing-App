from fastapi import APIRouter, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from app.database.db import get_db_connection
from app.models.booking import RideRequest, RideResponse, RideStatusUpdate
from app.utils.auth import get_current_user

router = APIRouter()

DISTANCE_MATRIX = {
    (1, 1): 8, (1, 2): 5, (1, 3): 7, (1, 4): 4, (1, 5): 6,
    (2, 1): 3, (2, 2): 6, (2, 3): 9, (2, 4): 2, (2, 5): 8,
    (3, 1): 5, (3, 2): 2, (3, 3): 4, (3, 4): 7, (3, 5): 3,
    (4, 1): 6, (4, 2): 9, (4, 3): 1, (4, 4): 5, (4, 5): 2,
    (5, 1): 7, (5, 2): 4, (5, 3): 8, (5, 4): 3, (5, 5): 1
}

def calculate_fare(distance):
    """Calculates ride fare based on distance-based pricing."""
    if distance == 1:
        return distance * 10000
    elif 2 <= distance <= 4:
        return distance * 15000
    else:
        return distance * 12000

def find_nearest_available_rider(user_id):
    """Finds the nearest available rider based on a fake distance matrix."""
    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id FROM riders WHERE status = 'Available'")
    available_riders = cursor.fetchall()

    cursor.close()
    conn.close()

    if not available_riders:
        return None

    nearest_rider = None
    min_distance = float("inf")

    for rider in available_riders:
        rider_id = rider["id"]
        distance = DISTANCE_MATRIX.get((user_id, rider_id), float("inf"))

        if distance < min_distance:
            min_distance = distance
            nearest_rider = rider_id

    return nearest_rider

@router.post("/book", response_model=RideResponse)
def book_ride(ride: RideRequest, current_user: dict = Depends(get_current_user)):
    """Books a ride and assigns the nearest available rider."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("SELECT id FROM users WHERE id = %s", (ride.user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=400, detail="User does not exist")

        rider_id = find_nearest_available_rider(ride.user_id)
        if not rider_id:
            raise HTTPException(status_code=400, detail="No available riders at the moment")

        fare = calculate_fare(ride.distance)

        cursor.execute(
            """
            INSERT INTO bookings (user_id, rider_id, status, distance, fare)
            VALUES (%s, %s, 'Pending', %s, %s) RETURNING id, user_id, rider_id, status, distance, fare
            """,
            (ride.user_id, rider_id, ride.distance, fare),
        )

        new_booking = cursor.fetchone()
        conn.commit()

        cursor.execute("UPDATE riders SET status = 'Busy' WHERE id = %s", (rider_id,))
        conn.commit()

        return RideResponse(**new_booking)

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cursor.close()
        conn.close()

@router.patch("/{booking_id}/status", response_model=RideResponse)
def update_booking_status(booking_id: int, status_update: RideStatusUpdate, current_user: dict = Depends(get_current_user)):
    """Updates ride status (Pending, In Progress, Completed, Canceled)."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("UPDATE bookings SET status = %s WHERE id = %s RETURNING *", (status_update.status, booking_id))
        updated_booking = cursor.fetchone()
        conn.commit()

        if not updated_booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        if status_update.status in ["Completed", "Canceled"]:
            cursor.execute("UPDATE riders SET status = 'Available' WHERE id = %s", (updated_booking["rider_id"],))
            conn.commit()

        return RideResponse(**updated_booking)

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cursor.close()
        conn.close()

@router.get("/{booking_id}/status", response_model=RideResponse)
def get_ride_status(booking_id: int, current_user: dict = Depends(get_current_user)):
    """Checks the status of a ride."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("SELECT * FROM bookings WHERE id = %s", (booking_id,))
        booking = cursor.fetchone()

        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        return RideResponse(**booking)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cursor.close()
        conn.close()
