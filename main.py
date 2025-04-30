from fastapi import FastAPI
from app.routes import user_routes, rider_routes, ride_routes, admin_routes
from app.database.init_db import create_tables

app = FastAPI()

@app.on_event("startup")
def startup():
    create_tables()

app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(rider_routes.router, prefix="/riders", tags=["Riders"])
app.include_router(ride_routes.router, prefix="/rides", tags=["Rides"])
app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])

@app.get("/")
def home():
    return {"message": "Ride Sharing API is running!"}
