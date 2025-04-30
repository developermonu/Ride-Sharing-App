from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    phone_number: str
    password: str
    is_admin: bool = False  # Add this field

class UserLogin(BaseModel):
    phone_number: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    phone_number: str
    is_admin: bool

class UserUpdate(BaseModel):
    name: str
    phone_number: str
    is_admin: bool
