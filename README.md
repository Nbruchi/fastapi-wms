# Waste Management System (WMS)

## Overview

The **Waste Management System (WMS)** is a web application built using **FastAPI** and **SQLAlchemy** for tracking waste types, collection points, scheduling, user management, and more. The system uses **JWT-based authentication** with **role-based access control (RBAC)** to ensure secure access to various functionalities. The backend connects to a **PostgreSQL** database with asynchronous support via **asyncpg**.

---

## Features

- **Role-Based Access Control (RBAC)**: Differentiates users based on their roles (e.g., Admin, Staff, User).
- **Authentication**: Secure JWT-based token authentication for API access.
- **Database**: PostgreSQL (asyncpg) as the database.
- **FastAPI**: The backend is built using the FastAPI framework for high-performance APIs.
- **Alembic**: Database migrations are managed using Alembic.

---

## Project Structure

```plaintext
app/
│
├── api/                  # Contains routes for various resources
│   ├── collection_points.py
│   ├── collection_records.py
│   ├── collection_schedules.py
│   ├── users.py          # User-related routes
│   └── waste_types.py
│
├── auth.py               # Handles authentication logic (JWT)
├── db/                   # Database-related files
│   ├── database.py       # Database session and connection
│   ├── models.py         # SQLAlchemy models
│   └── logs.py           # Database log model
├── utils/                # Utility functions
│   └── utils.py          # Helper functions (e.g., password hashing, token creation)
├── main.py               # FastAPI application entry point
└── .env                  # Environment variables (database URL, secret keys, etc.)
```

---

## Requirements

The project uses Python 3.8+ and the following dependencies:

```plaintext
aiohappyeyeballs==2.4.3
aiohttp==3.10.10
alembic==1.14.0
asyncpg==0.30.0
bcrypt==4.2.0
fastapi==0.115.5
fastapi-users==14.0.0
fastapi-users-db-sqlalchemy==6.0.1
psycopg2==2.9.10
PyJWT==2.9.0
sqlalchemy==2.0.36
uvicorn==0.32.0
```

### Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Ensure that the following environment variables are set in a `.env` file in the root of the project:

```plaintext
DATABASE_URL=postgresql+asyncpg://<username>:<password>@localhost:5432/<database_name>
ACCESS_TOKEN_SECRET=<your-secret-key-here>
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace `<your-secret-key-here>` with a strong, random secret key for JWT authentication. And replace `<username>, <password>` and `<database_name>` with suitable ones from your configurations

---

## Database Setup and Migration

1. **Create a PostgreSQL Database**: Ensure PostgreSQL is installed and create a database (e.g., `wms`).
   
2. **Run Alembic Migrations**:
   Alembic is used for database migrations. To apply the migrations, run:

   ```bash
   alembic upgrade head
   ```

3. **Run the Application**:
   After applying the migrations, run the FastAPI application with:

   ```bash
   uvicorn main:app --reload
   ```

---

## Authentication

This project uses JWT for user authentication. To access protected endpoints, users must first log in and obtain a JWT token.

### Example Login

```bash
POST /auth/login
```

Request body:

```json
{
  "username": "new_user",
  "password": "password123"
}
```

Response body:

```json
{
  "access_token": "<your-jwt-token>",
  "token_type": "bearer"
}
```

### Access Protected Routes

Once you have the JWT token, include it in the `Authorization` header for all protected endpoints:

```bash
GET /admin-dashboard
Authorization: Bearer <your-jwt-token>
```

---

## Role-Based Access Control (RBAC)

The application supports role-based access control to restrict access to certain resources based on the user's role. For example, only users with the `admin` role can access the `/admin-dashboard` endpoint.

To secure routes based on roles, the `role_required` decorator is used:

```python
from fastapi import APIRouter, Depends
from app.utils.utils import role_required
from app.db.models import User

router = APIRouter()

@router.get("/admin-dashboard")
async def admin_dashboard(current_user: User = Depends(role_required(["admin"]))):
    return {"message": "Welcome to the admin dashboard"}
```

---

## Models

The `User` model is defined in `app/db/models.py`, where it includes fields like `id`, `username`, `hashed_password`, and `role`. Here’s an example of how the `User` model might look:

```python
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
```

---

## Utilities

The utilities in `app/utils/utils.py` provide key functions for the application:

- **Password Hashing**: Functions to hash and verify passwords using `bcrypt`.
- **JWT Token Creation**: Function to generate access tokens with an expiration time.
- **Role Checking**: The `role_required` decorator to enforce role-based access control.

Example of the `role_required` function:

```python
from fastapi import HTTPException, Depends
from app.auth import get_current_user
from app.db.models import User
from fastapi import status

def role_required(required_roles: list[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return current_user
    return role_checker
```

---

## Running the Application Locally

To start the FastAPI server locally, run the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

This will run the application at `http://localhost:8000`. You can access the interactive API documentation at:

- [Swagger UI](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---