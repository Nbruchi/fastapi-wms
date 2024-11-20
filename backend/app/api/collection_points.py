from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from sqlalchemy import exists
from sqlalchemy import select,delete
from app.db.models import (CollectionPoint, CollectionPointCreate,CollectionPointUpdate,CollectionPointInDb, LogEntry)

collection_points_router = APIRouter(prefix="/collection-points")

async def collection_point_exists(db:AsyncSession = Depends(get_db),collection_point_id:int = None) -> bool:
    result = await db.execute(select(exists().where(CollectionPointInDb.id == collection_point_id)))
    return result.scalar()

@collection_points_router.get("/",response_model=list[CollectionPointInDb])
async def get_collection_points(db: AsyncSession = Depends(get_db)):
    try:
        collection_points = await db.query(CollectionPointInDb).all()
        return collection_points
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to get collection points: {str(e)}")
    

@collection_points_router.post("/",response_model=CollectionPointInDb,status_code=status.HTTP_201_CREATED)
async def create_collection_point(collection_point: CollectionPointCreate,db: AsyncSession = Depends(get_db)):
    try:
        new_collection_point = CollectionPointInDb(**collection_point.model_dump()) 
        db.add(new_collection_point)
        await db.commit()
        await db.refresh(new_collection_point)
        return new_collection_point
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to create collection point: {str(e)}")
    
@collection_points_router.get("/{collection_point_id}", response_model=CollectionPointInDb)
async def get_collection_point(collection_point_id:int,db:AsyncSession = Depends(get_db)):
    try:
        collection_point = await db.get(CollectionPointInDb,collection_point_id)
        if collection_point is None:
            raise HTTPException(status_code=404,detail="Collection point not found")
        return collection_point
    except Exception as e:    
        raise HTTPException(status_code=500,detail=f"Failed to get collection point: {str(e)}")
    

@collection_points_router.put("/{collection_point_id}",response_model=CollectionPointInDb,status_code=status.HTTP_200_OK)
async def update_collection_point(collection_point_id: int,collection_point: CollectionPointUpdate,db: AsyncSession = Depends(get_db)):
    try:
        db_collection_point = await db.get(CollectionPointInDb,collection_point_id)
        if db_collection_point is None:
            raise HTTPException(status_code=404,detail="Collection point not found")
        for key,value in collection_point.model_dump().items():
            setattr(db_collection_point,key,value)
        await db.commit()
        await db.refresh(db_collection_point)
        return db_collection_point
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to update collection point: {str(e)}")
    

@collection_points_router.delete("/{collection_point_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection_point(collection_point_id: int,db: AsyncSession = Depends(get_db)):
    try:
        db_collection_point = await db.get(CollectionPointInDb,collection_point_id)
        if db_collection_point is None:
            raise HTTPException(status_code=404,detail="Collection point not found")
        log_entry = LogEntry(
            action="delete",
            entity_type="CollectionPoint",
            entity_id=str(collection_point_id),
            data = db_collection_point.__dict__
        )
        await db.add(log_entry)
        await db.delete(db_collection_point)
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to delete collection point: {str(e)}")
    
@collection_points_router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_collection_points(db: AsyncSession = Depends(get_db)):
    try:
        statement = delete(CollectionPoint)
        await db.execute(statement)
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to delete all collection points: {str(e)}")