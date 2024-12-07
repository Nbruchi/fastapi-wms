from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.schedule import create_schedule, get_schedule, update_schedule, delete_schedule, get_all_schedules,get_paginated_schedules
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleOut
from app.database import get_db
from sqlalchemy import select, func
from uuid import UUID
from app.models.schedule import Schedule

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



@router.get("/all", response_model=dict)
async def read_paginated_schedules(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    try:
        # Fetch total count of schedules
        total_query = await db.execute(select(func.count(Schedule.id)))
        total_items = total_query.scalar_one()

        # Fetch paginated schedules
        schedules = await get_paginated_schedules(db, skip=skip, limit=limit)
        
        return {"schedules": schedules, "total": total_items}
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

