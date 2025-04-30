# Ride Sharing App

A microservices-based ride sharing platform built with FastAPI and PostgreSQL. This project demonstrates a scalable backend architecture for a ride-hailing service, including user registration, authentication, ride booking, rider management, and admin features.

---

## Features

- **User Registration & Login:** Secure authentication with JWT tokens.
- **Rider Registration & Management:** Riders can register, update status (Available/Busy), and be assigned to rides.
- **Ride Booking:** Users can book rides, system assigns the nearest available rider, and calculates fare based on distance.
- **Admin Dashboard:** Admins can view and manage users, riders, and rides.
- **Database:** PostgreSQL with automatic table creation and sample data seeding.
- **Dockerized:** Easily deployable using Docker and Docker Compose.

---

## Architecture

- **FastAPI** for REST APIs.
- **PostgreSQL** as the database.
- **Microservices**: Separate modules for users, riders, rides, and admin.
- **JWT Authentication** for secure endpoints.
- **Docker** for containerization and easy deployment.

---

## Project Structure

```
.
├── app/                # Main FastAPI application and routes
├── service/            # Microservice modules (users, rider, rides, admin)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker build file
├── docker-compose.yml  # Multi-container orchestration
├── .env                # Environment variables
└── README.md           # Project documentation
```

---

## Screenshots

### Output

![Output Screenshot](screenshots/Screenshot%202025-04-30%20at%2013-33-59%20FastAPI%20-%20Swagger%20UI.png)

> The above screenshot shows the API documentation for the Ride Sharing App, including endpoints for users, riders, rides, and admin, as well as the data schemas.

---

## Installation & Running (via GitHub)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/developermonu/Ride-Sharing-App.git
   cd Ride-Sharing-App
   ```

2. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in the required values, or use the provided `.env`.

3. **Build and start the services using Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Access the API:**
   - The FastAPI server will be running at [http://localhost:8000](http://localhost:8000)
   - API docs available at [http://localhost:8000/docs](http://localhost:8000/docs)

5. **Stopping the services:**
   ```bash
   docker-compose down
   ```

---

## API Endpoints

- `/users/register` - Register a new user
- `/users/login` - User login (returns JWT)
- `/riders/register` - Register as a rider
- `/rides/book` - Book a ride
- `/admin/dashboard` - Admin dashboard (JWT required)

> See the OpenAPI docs at `/docs` for full details.

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License.

