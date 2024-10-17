# Single-database configuration for Flask.
## Overview

The room Booking API is a Flask-based backend application designed to manage room bookings in swift hotel. It provides endpoints for users to search for available rooms and manage reservations.

## Directory Structure
project_root/ ├── app/ # Core application code and modules ├── instance/ # SQLite database file │ └── app.db ├── migrations/ # Database migration scripts ├── swift_booking/ # (Add description if applicable) ├── venv/ # Virtual environment for dependencies ├── .env # Environment variables for configuration ├── .gitignore # Files and directories to ignore in Git ├── config.py # Application configuration settings ├── makemigrations.sh # Script for managing migrations ├── requirements.txt # Python dependencies ├── run.py # Entry point for the application ├── seed.py # Script to populate the database with initial data └── README.md # Project documentation

## Key Features

- **User Management**: Handle user registration, authentication, and profile management.
- **Room Management**: CRUD operations for room listings, including availability and pricing.
- **Booking System**: Manage customer bookings, including creation, updates, and cancellations.
- **Payment Processing**: Integrate payment systems to facilitate secure transactions.

## Setup

1. Clone the repository:
   ```bash
  ` git clone git@github.com:Snappyhacker/Phase4backend.git`
   cd Phase4backend
Create a virtual environment:

bash

`python -m venv venv`
`source venv/bin/activate ` # For macOS/Linux
`venv\Scripts\activate`  # For Windows
Install dependencies:

Copy code
`pip install -r requirements.txt`
Create the database and apply migrations:

Copy code
`flask db init`
`flask db migrate -m "Initial migration"`
`flask db upgrade`
Seed the database (optional):

bash
Copy code
python seed.py
Run the application:
Copy code
`python run.py`
API Endpoints
(Add your API endpoints here with descriptions. Example:)

GET /api/rooms: Retrieves a list of all hotels.
POST /api/bookings: Creates a new booking.
