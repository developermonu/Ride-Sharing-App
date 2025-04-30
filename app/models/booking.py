from pydantic import BaseModel

class RideRequest(BaseModel):
    """Schema for requesting a ride."""
    user_id: int
    distance: int  # Distance in KM

class RideResponse(BaseModel):
    """Schema for returning ride details."""
    id: int
    user_id: int
    rider_id: int
    status: str
    distance: int
    fare: int

class RideStatusUpdate(BaseModel):
    """Schema for updating ride status."""
    status: str  # Pending, In Progress, Completed, Canceled
