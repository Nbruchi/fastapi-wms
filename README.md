# 🌍 FastAPI WMS

The **Waste Management System (WMS)** is a **FastAPI-powered** backend application designed to streamline waste management operations. It allows users to manage recycle logs, reports, and schedules, with efficient database operations powered by **PostgreSQL** and **Alembic** for migrations.

---

## 📂 Project Structure

```plaintext
alembic/                        # Alembic migrations
    ├── env.py                   # Migration environment config
    └── versions/                # Migration scripts

app/                             # Application source code
    ├── __init__.py              # Initialize app module
    ├── database.py              # Database connection and session management
    ├── main.py                  # FastAPI entry point
    ├── models/                  # SQLAlchemy models
    ├── routers/                 # API routes (controllers)
    ├── schemas/                 # Pydantic models (validation)
    ├── services/                # Business logic
database_update.py               # Database update script
requirements.txt                # Project dependencies
```

---

## 📋 Requirements

Make sure you have the following dependencies installed:

```bash
pip install -r requirements.txt
```

Dependencies in `requirements.txt` include:
- **FastAPI** for the API framework
- **SQLAlchemy** and **asyncpg** for database interactions
- **Alembic** for migrations

---

## ⚙️ Setup & Running the Application

### 1. Set up the Database
- Update the `DATABASE_URL` in `app/database.py` with your PostgreSQL credentials.

### 2. Run Database Migrations
Initialize the database schema with Alembic:

```bash
alembic upgrade head
```

### 3. Start the FastAPI Server
Start the application using Uvicorn:

```bash
uvicorn main:app --reload
```

The application will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## 🔑 Authentication (Planned Feature)

The application does not yet include authentication or role-based access control (RBAC). However, future updates will integrate **JWT**-based authentication and **RBAC** to manage user roles and secure access to specific endpoints.

---

## 🛠️ Development Tips

- **Database Setup**: Use `alembic` to handle migrations and ensure your database schema is in sync.
- **Testing**: Use FastAPI’s built-in test client and pytest to create automated tests for your API.
- **Logging**: Implement logging to track API activity, which is useful for debugging and auditing.

---

## 💻 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more information.

---

## 📄 Documentation

Explore API documentation directly via:

- [Swagger UI](http://127.0.0.1:8000/docs)  
- [ReDoc](http://127.0.0.1:8000/redoc)

---

### Why This Project?

The **Waste Management System (WMS)** aims to simplify the process of tracking and managing recycling activities, ensuring smooth operations and data management for waste collection schedules and reports. Whether you're a developer or waste management professional, this system will help manage your operations effectively.