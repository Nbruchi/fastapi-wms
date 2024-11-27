# update_database.py

import asyncio
from sqlalchemy import create_engine, Column, String, Float, DateTime, UUID, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select

from app.database import DATABASE_URL  # Your async database URL
from app.models.recycle import Recycle
from app.models.schedule import Schedule

# Define your models
Base = declarative_base()

# Use AsyncSession and create_async_engine for async operations
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def update_database():
    async with Session() as session:
        try:
            print("Adding schedule_id column to recycle table...")

            # Fetch a schedule for updating (this could be modified to suit your needs)
            result = await session.execute(select(Schedule).limit(1))  # Async query using select
            first_schedule = result.scalars().first()  # Get the first schedule (if any)

            if first_schedule:
                print(f"Found schedule: {first_schedule.id}")

                # Update recycle table with the schedule_id (use async update)
                await session.execute(
                    Recycle.__table__.update().values(schedule_id=first_schedule.id)
                )

                # Commit the changes
                await session.commit()
                print("Recycle table updated with schedule_id.")
            else:
                print("No schedules found, skipping update.")
        except Exception as e:
            print(f"Error during database update: {e}")
            await session.rollback()

# Run the async update function
if __name__ == "__main__":
    asyncio.run(update_database())
