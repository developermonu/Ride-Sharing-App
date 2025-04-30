from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    name: str
    phone_number: str
    is_admin: bool

class RiderResponse(BaseModel):
    id: int
    user_id: int
    vehicle_type: str
    license_plate: str
    status: str

class RideResponse(BaseModel):
    id: int
    user_id: int
    rider_id: int
    status: str
    distance: int
    fare: int
