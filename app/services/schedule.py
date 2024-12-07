from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleOut


async def create_schedule(db: AsyncSession, schedule: ScheduleCreate):
    db_schedule = Schedule(**schedule.model_dump())
    db.add(db_schedule)
    await db.commit()
    await db.refresh(db_schedule)
    return db_schedule



async def get_all_schedules(db: AsyncSession):
    result = await db.execute(select(Schedule))
    schedules = result.scalars().all()  # Extracts the actual objects from the result
    return [ScheduleOut.from_orm(schedule) for schedule in schedules]



async def get_paginated_schedules(db: AsyncSession, skip: int = 0, limit: int = 50) -> list[ScheduleOut]:
    result = await db.execute(select(Schedule).offset(skip).limit(limit))
    schedules = result.scalars().all()
    return [ScheduleOut.from_orm(schedule) for schedule in schedules]



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