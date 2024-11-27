from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.schedule import create_schedule, get_schedule, update_schedule, delete_schedule, get_all_schedules
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleOut
from app.database import get_db
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=ScheduleOut)
async def create_schedule_endpoint(schedule: ScheduleCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_schedule(db, schedule)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/", response_model=List[ScheduleOut])
async def read_schedules(db: AsyncSession = Depends(get_db)):
    try:
        # Fetching schedules through service
        schedules = await get_all_schedules(db)
        return schedules
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{schedule_id}", response_model=ScheduleOut)
async def read_schedule(schedule_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        db_schedule = await get_schedule(db, schedule_id)
        if db_schedule is None:
            raise HTTPException(status_code=404, detail="Schedule not found")
        return db_schedule
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{schedule_id}", response_model=ScheduleOut)
async def update_schedule_endpoint(schedule_id: UUID, schedule_update: ScheduleUpdate, db: AsyncSession = Depends(get_db)):
    try:
        db_schedule = await update_schedule(db, schedule_id, schedule_update)
        if db_schedule is None:
            raise HTTPException(status_code=404, detail="Schedule not found")
        return db_schedule
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{schedule_id}", response_model=ScheduleOut)
async def delete_schedule_endpoint(schedule_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        db_schedule = await delete_schedule(db, schedule_id)
        if db_schedule is None:
            raise HTTPException(status_code=404, detail="Schedule not found")
        return db_schedule
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
