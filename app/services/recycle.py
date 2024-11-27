from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.recycle import Recycle
from app.models.schedule import Schedule
from uuid import UUID
from app.schemas.recycle import RecycleCreate, RecycleUpdate, RecycleOut
from fastapi import HTTPException, status


async def create_recycle(db: AsyncSession, recycle: RecycleCreate):
    # Check if the schedule_id exists in the schedules table
    result = await db.execute(select(Schedule).filter(Schedule.id == recycle.schedule_id))
    db_schedule = result.scalar_one_or_none()

    if db_schedule is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid schedule_id, schedule not found")

    # Proceed to create the recycle entry
    db_recycle = Recycle(**recycle.model_dump())
    db.add(db_recycle)
    await db.commit()
    await db.refresh(db_recycle)
    return db_recycle


async def get_recycles(db: AsyncSession):
    # Execute the query with offset and limit
    result = await db.execute(select(Recycle))
    recycles = result.scalars().all()

    return [RecycleOut.model_validate(recycle) for recycle in recycles]


async def get_recycle(db: AsyncSession, recycle_id: UUID):
    result = await db.execute(select(Recycle).filter(Recycle.id == recycle_id))
    return result.scalar_one_or_none()


async def update_recycle(db: AsyncSession, recycle_id: UUID, recycle_update: RecycleUpdate):
    # Check if the recycle entry exists
    db_recycle = await get_recycle(db, recycle_id)
    if db_recycle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recycle entry not found")

    # If there's a schedule_id in the update, validate it
    if recycle_update.schedule_id:
        result = await db.execute(select(Schedule).filter(Schedule.id == recycle_update.schedule_id))
        db_schedule = result.scalar_one_or_none()

        if db_schedule is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid schedule_id, schedule not found")

    # Update fields
    for key, value in recycle_update.model_dump(exclude_unset=True).items():
        setattr(db_recycle, key, value)

    # Commit and refresh the updated recycle entry
    await db.commit()
    await db.refresh(db_recycle)
    return db_recycle

async def delete_recycle(db: AsyncSession, recycle_id: UUID):
    db_recycle = await get_recycle(db, recycle_id)
    if db_recycle:
        await db.delete(db_recycle)
        await db.commit()
        return db_recycle
    return None
