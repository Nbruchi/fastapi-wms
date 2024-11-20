# ♻️ Waste Management System (WMS)

## 📘 Overview

The **Waste Management System (WMS)** is a web application built with **FastAPI** and **SQLAlchemy** to track waste types, manage collection points and schedules, and handle user management. It features **JWT-based authentication** and **Role-Based Access Control (RBAC)** for secure and segmented access. The backend is supported by **PostgreSQL** with asynchronous capabilities via **asyncpg**.

---

## 🌟 Features

- **🔐 Role-Based Access Control (RBAC)**: Distinguishes between user roles (Admin, Staff, User).
- **🔑 Secure Authentication**: JWT-based token authentication for safe API usage.
- **💾 Database**: PostgreSQL with `asyncpg` for async support.
- **🚀 FastAPI Framework**: High-performance backend architecture.
- **🔧 Alembic Integration**: Easy database migrations.

---

## 📂 Project Structure

```plaintext
app/
│
├── api/                  # API routes for resources
│   ├── collection_points.py
│   ├── collection_records.py
│   ├── collection_schedules.py
│   ├── users.py          # User-specific routes
│   └── waste_types.py
│
├── auth.py               # JWT authentication logic
├── db/                   # Database setup and models
│   ├── database.py       # DB connection and session
│   ├── models.py         # SQLAlchemy ORM models
│   └── logs.py           # Log model for activity tracking
│
├── utils/                # Utility scripts
│   └── utils.py          # Helper functions (password hashing, JWT creation)
│
├── main.py               # FastAPI app entry point
└── .env                  # Environment variable configuration
```

---

## 📝 Requirements

**Python**: 3.8+  
Below are the core dependencies used:

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

### ⚙️ Installation

To install dependencies, run:

```bash
pip install -r requirements.txt
```

---

## 🔧 Environment Variables

Create a `.env` file in the project root and set the following:

```plaintext
DATABASE_URL=postgresql+asyncpg://<username>:<password>@localhost:5432/<database_name>
ACCESS_TOKEN_SECRET=<your-secret-key>
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace `<username>`, `<password>`, and `<database_name>` with your database credentials. Ensure `<your-secret-key>` is a strong, random string.

---

## 🛠️ Database Setup & Migration

1. **Create a PostgreSQL Database**: Ensure PostgreSQL is running and create a database (e.g., `wms`).

2. **Run Alembic Migrations**:

   ```bash
   alembic upgrade head
   ```

3. **Start the Application**:
   ```bash
   uvicorn main:app --reload
   ```

---

## 🔑 Authentication

JWT is used for user authentication. Users must log in to obtain an access token for protected endpoints.

### Login Example

**Request**:

```bash
POST /auth/login
```

**Request Body**:

```json
{
  "username": "new_user",
  "password": "password123"
}
```

**Response**:

```json
{
  "access_token": "<your-jwt-token>",
  "token_type": "bearer"
}
```

### Using the Token

Include the JWT token in the `Authorization` header for accessing protected routes:

```bash
GET /admin-dashboard
Authorization: Bearer <your-jwt-token>
```

---

## 🛡️ Role-Based Access Control (RBAC)

RBAC restricts access based on user roles (e.g., only admins can access `/admin-dashboard`).

### Example of Securing Routes

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

## 📚 Models

The `User` model in `app/db/models.py` includes fields such as `id`, `username`, `hashed_password`, and `role`.

### User Model Example:

```python
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
```

---

## 🔧 Utilities

Utilities in `app/utils/utils.py` support the core logic:

- **🔒 Password Hashing**: Secure password hashing and verification using `bcrypt`.
- **🔑 JWT Creation**: Functions to generate tokens with expiration settings.
- **🛡️ Role Checks**: `role_required` decorator for enforcing role-specific access.

### Example `role_required` Function:

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

## ▶️ Running the Application Locally

Start the server with:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Swagger UI** and **ReDoc** are available for API exploration:

- [Swagger UI](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)

---

## ⚖️ License

Licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
