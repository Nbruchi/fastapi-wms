from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db,entity_exists
from app.db.models import (
    CollectionSchedule, 
    CollectionScheduleCreate,
    CollectionScheduleUpdate,
    CollectionScheduleInDb,
    CollectionPointInDb, 
    LogEntry,
    WasteTypeInDb
)

collection_schedules_router = APIRouter(prefix="/collection-schedules")

@collection_schedules_router.get("/",response_model=list[CollectionScheduleInDb])
async def get_collection_schedules(db: AsyncSession = Depends(get_db)):
    try:
        collection_schedules = await db.query(CollectionScheduleInDb).all()
        return collection_schedules
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to get collection schedules: {str(e)}")
    
@collection_schedules_router.post("/",response_model=CollectionScheduleInDb,status_code=status.HTTP_201_CREATED)
async def create_collection_schedule(collection_schedule: CollectionScheduleCreate,db: AsyncSession = Depends(get_db)):
    try:
        if not await entity_exists(db,WasteTypeInDb,collection_schedule.waste_type_id):
            raise HTTPException(status_code=404,detail="Waste type not found")
        if not await entity_exists(db,CollectionPointInDb,collection_schedule.collection_point_id):
            raise HTTPException(status_code=404,detail="Collection point not found")
        new_collection_schedule = CollectionScheduleInDb(**collection_schedule.model_dump()) 
        db.add(new_collection_schedule)
        await db.commit()
        await db.refresh(new_collection_schedule)
        return new_collection_schedule
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to create collection schedule: {str(e)}")
    
@collection_schedules_router.get("/{collection_schedule_id}",response_model=CollectionScheduleInDb)
async def get_collection_schedule(collection_schedule_id: int,db: AsyncSession = Depends(get_db)):
    try:
        collection_schedule = await db.get(CollectionScheduleInDb,collection_schedule_id)
        if not await entity_exists(db,WasteTypeInDb,collection_schedule.waste_type_id):
            raise HTTPException(status_code=404,detail="Waste type not found")
        if not await entity_exists(db,CollectionPointInDb,collection_schedule.collection_point_id):
            raise HTTPException(status_code=404,detail="Collection point not found")
        if collection_schedule is None:
            raise HTTPException(status_code=404,detail="Collection schedule not found")
        return collection_schedule
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to get collection schedule: {str(e)}")


@collection_schedules_router.put("/{collection_schedule_id}",response_model=CollectionScheduleInDb,status_code=status.HTTP_200_OK)
async def update_collection_schedule(collection_schedule_id: int,collection_schedule: CollectionScheduleUpdate,db: AsyncSession = Depends(get_db)):
    try:
        db_collection_schedule = await db.get(CollectionScheduleInDb,collection_schedule_id)
        if not await entity_exists(db,WasteTypeInDb,db_collection_schedule.waste_type_id):
            raise HTTPException(status_code=404,detail="Waste type not found")
        if not await entity_exists(db,CollectionPointInDb,db_collection_schedule.collection_point_id):
            raise HTTPException(status_code=404,detail="Collection point not found")
        if db_collection_schedule is None:
            raise HTTPException(status_code=404,detail="Collection schedule not found")
        for key,value in collection_schedule.model_dump().items():
            setattr(db_collection_schedule,key,value)
        await db.commit()
        await db.refresh(db_collection_schedule)
        return db_collection_schedule
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to update collection schedule: {str(e)}")    

    
@collection_schedules_router.delete("/{collection_schedule_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection_schedule(collection_schedule_id: int,db: AsyncSession = Depends(get_db)):
    try:
        db_collection_schedule = await db.get(CollectionScheduleInDb,collection_schedule_id)
        if not await entity_exists(db,WasteTypeInDb,db_collection_schedule.waste_type_id):
            raise HTTPException(status_code=404,detail="Waste type not found")
        if not await entity_exists(db,CollectionPointInDb,db_collection_schedule.collection_point_id):
            raise HTTPException(status_code=404,detail="Collection point not found")
        if db_collection_schedule is None:
            raise HTTPException(status_code=404,detail="Collection schedule not found")
        log_entry = LogEntry(
            action="delete",
            entity_type="CollectionSchedule",
            entity_id=str(collection_schedule_id),
            data = db_collection_schedule.__dict__
        )
        await db.add(log_entry)
        await db.delete(db_collection_schedule)
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to delete collection schedule: {str(e)}")
    
@collection_schedules_router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_collection_schedules(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(delete(CollectionSchedule))
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to delete all collection schedules: {str(e)}")