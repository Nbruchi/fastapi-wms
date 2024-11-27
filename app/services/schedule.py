from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleOut

# Existing functions

async def create_schedule(db: AsyncSession, schedule: ScheduleCreate):
    db_schedule = Schedule(**schedule.model_dump())
    db.add(db_schedule)
    await db.commit()
    await db.refresh(db_schedule)
    return db_schedule

async def get_schedule(db: AsyncSession, schedule_id: UUID):
    result = await db.execute(select(Schedule).filter(Schedule.id == schedule_id))
    return result.scalar_one_or_none()

async def update_schedule(db: AsyncSession, schedule_id: UUID, schedule_update: ScheduleUpdate):
    db_schedule = await get_schedule(db, schedule_id)
    if db_schedule:
        for key, value in schedule_update.model_dump(exclude_unset=True).items():
            setattr(db_schedule, key, value)
        await db.commit()
        await db.refresh(db_schedule)
        return db_schedule
    return None

async def delete_schedule(db: AsyncSession, schedule_id: UUID):
    db_schedule = await get_schedule(db, schedule_id)
    if db_schedule:
        await db.delete(db_schedule)
        await db.commit()
        return db_schedule
    return None

# New function to fetch all schedules
async def get_all_schedules(db: AsyncSession):
    result = await db.execute(select(Schedule))
    schedules = result.scalars().all()  # Extracts the actual objects from the result
    return [ScheduleOut.model_validate(schedule) for schedule in schedules]
