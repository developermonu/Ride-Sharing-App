from pydantic import BaseModel

class RiderCreate(BaseModel):
    """Schema for creating a Rider."""
    user_id: int
    vehicle_type: str
    license_plate: str

class RiderResponse(BaseModel):
    """Schema for returning Rider information."""
    id: int
    user_id: int
    vehicle_type: str
    license_plate: str
    status: str = "Available"

class RiderStatusUpdate(BaseModel):
    """Schema for updating Rider availability status."""
    status: str  # Available, Busy
