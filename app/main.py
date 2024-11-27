from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import recycle, report, schedule
from app.database import test_connection  # Import the test_connection function

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recycle.router, prefix="/recycles", tags=["Recycles"])
app.include_router(report.router, prefix="/reports", tags=["Reports"])
app.include_router(schedule.router, prefix="/schedules", tags=["Schedules"])


# Use app.lifecycle to handle startup events
@app.on_event("startup")
async def on_startup():
    print("🟡 Testing database connection...")
    await test_connection()  # Test the database connection at startup
    print("🟢 Database connection test completed.")
