# Ride Sharing System with FastAPI

## Table of Contents
- [Overview](#overview)
- [Core Services](#core-services)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Architecture](#architecture)
- [API Development](#api-development)
- [Database Design](#database-design)
- [Testing](#testing)
- [Documentation](#documentation)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running Tests](#running-tests)
- [Contributing](#contributing)

## Overview

The ride-sharing system allows users to request rides and be matched with the nearest available riders. Similar to services like a ride-sharing platform, this system handles user registration, rider management, ride booking, fare calculation, and ride status updates. The backend-only microservices system is built using FastAPI, applying system design and API development principles to create a scalable, performant, and efficient ride-hailing application.

## Core Services
The ride-sharing system consists of the following core services:

1. **User Service**: Manages user registration, authentication, and profile management.
2. **Rider Service**: Manages rider registration, authentication, and profile management.
3. **Ride Service**: Handles ride booking, fare calculation, and ride status updates.
4. **Notification Service**: Sends notifications to users and riders about ride status updates.
5. **Payment Service**: Manages payment processing and fare transactions.

## Tech Stack
The ride-sharing system is built using the following technologies:

- **FastAPI**: For building the RESTful APIs.
- **PostgreSQL**: For data storage and management.
- **Docker**: For containerization and deployment.
- **Kafka**: For messaging and event streaming (optional).
- **Pytest**: For testing the application.
- **OpenAPI/Swagger**: For API documentation.

## Features
The system includes:
+ User registration and ride booking.
+ Rider registration and acceptance of ride requests.
+ Fare calculation based on a tiered distance pricing model.
+ Tracking of ride status updates (_Pending, In Progress, Completed, Cancelled_).
+ Data storage in a PostgreSQL database.
+ Optional Kafka integration for messaging.

## Architecture
The software architecture is documented using the **C4 Model**, including the following diagrams:
- **Context Diagram**: Overview of the system and its interactions with the user and external components.
- **Container Diagram**: High-level components such as FastAPI services and external systems.
- **Component Diagram**: Breakdown of each container into its components and their interactions.
- **Code Diagram**: Detailed design of the code structure within each component.

## API Development
The system's RESTful APIs are developed using FastAPI, with endpoints for user and rider registration, ride booking, fare calculation, and ride status updates.

## Database Design
The PostgreSQL database schema is designed to store user, rider, and ride information, ensuring data integrity and efficient querying.

## Testing
The system includes unit tests for individual components and integration tests for API endpoints.

## Documentation
API endpoints are documented using OpenAPI/Swagger, with clear instructions on how to set up and run the system.

## Getting Started
### Prerequisites
- Python 3.8+
- PostgreSQL
- FastAPI
- Docker (optional, for containerization)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/ride-sharing-app.git
    cd ride-sharing-app
    ```

2. Set up a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Set up the PostgreSQL database and update the database URL in the configuration file.

4. Run the FastAPI application:
    ```bash
    uvicorn app.main:app --reload
    ```

### Running Tests
Run the test suite using pytest:
```bash
pytest
```

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.


