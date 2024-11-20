from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.db.database import get_db,entity_exists
from app.db.models import (
    CollectionRecordCreate,
    CollectionRecordUpdate,
    CollectionRecordInDb,
    CollectionScheduleInDb,
    LogEntry,
    CollectionRecord
)

collection_records_router = APIRouter(prefix="/collection-records")


@collection_records_router.post("/",response_model=CollectionRecordInDb,status_code=status.HTTP_201_CREATED)
async def create_collection_record(collection_record: CollectionRecordCreate,db: AsyncSession = Depends(get_db)):
    try:
        if not await entity_exists(db,CollectionScheduleInDb,collection_record.collection_schedule_id):
            raise HTTPException(status_code=404,detail="Collection schedule not found")
        new_collection_record = CollectionRecordInDb(**collection_record.model_dump()) 
        db.add(new_collection_record)
        await db.commit()
        await db.refresh(new_collection_record)
        return new_collection_record
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to create collection record: {str(e)}")
    
@collection_records_router.get("/",response_model=list[CollectionRecordInDb])
async def get_collection_records(db: AsyncSession = Depends(get_db)):
    try:
        collection_records = await db.query(CollectionRecordInDb).all()
        return collection_records
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to get collection records: {str(e)}")
    
@collection_records_router.get("/{collection_record_id}",response_model=CollectionRecordInDb)
async def get_collection_record(collection_record_id: int,db: AsyncSession = Depends(get_db)):
    try:
        collection_record = await db.get(CollectionRecordInDb,collection_record_id)
        if collection_record is None:
            raise HTTPException(status_code=404,detail="Collection record not found")
        if not await entity_exists(db,CollectionScheduleInDb,collection_record.collection_schedule_id):
            raise HTTPException(status_code=404,detail="Collection schedule not found")
        return collection_record
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to get collection record: {str(e)}")
    

@collection_records_router.put("/{collection_record_id}",response_model=CollectionRecordInDb)
async def update_collection_record(collection_record_id: int,collection_record: CollectionRecordUpdate,db: AsyncSession = Depends(get_db)):
    try:
        db_collection_record = await db.get(CollectionRecordInDb,collection_record_id)
        if db_collection_record is None:
            raise HTTPException(status_code=404,detail="Collection record not found")
        if not await entity_exists(db,CollectionScheduleInDb,collection_record.collection_schedule_id):
            raise HTTPException(status_code=404,detail="Collection schedule not found")
        for field,value in collection_record.model_dump().items():
            setattr(db_collection_record,field,value)
        await db.commit()
        await db.refresh(db_collection_record)
        return db_collection_record
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to update collection record: {str(e)}")
    
@collection_records_router.delete("/{collection_record_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection_record(collection_record_id: int,db: AsyncSession = Depends(get_db)):
    try:
        db_collection_record = await db.get(CollectionRecordInDb,collection_record_id)
        if db_collection_record is None:
            raise HTTPException(status_code=404,detail="Collection record not found")
        log_entry = LogEntry(
            action="delete",
            entity_type="CollectionRecord",
            entity_id=str(collection_record_id),
            data = db_collection_record.__dict__
        )
        await db.add(log_entry)
        await db.delete(db_collection_record)
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to delete collection record: {str(e)}")
    
@collection_records_router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_collection_records(db: AsyncSession = Depends(get_db)):
    try:
        statement = delete(CollectionRecord)
        await db.execute(statement)
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to delete all collection records: {str(e)}")