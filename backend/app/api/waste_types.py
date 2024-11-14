from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from sqlalchemy import exists
from sqlalchemy.future import select
from app.db.models import (LogEntry, WasteTypeCreate,WasteTypeUpdate,WasteTypeInDb)

waste_types_router = APIRouter(prefix="/waste-types")

async def waste_type_exists(db:AsyncSession = Depends(get_db),waste_type_id:int = None) -> bool:
    result = await db.execute(select(exists().where(WasteTypeInDb.id == waste_type_id)))
    return result.scalar()

@waste_types_router.get("/",response_model=list[WasteTypeInDb])
async def get_waste_types(db: AsyncSession = Depends(get_db)):
    try:
        waste_types = await db.query(WasteTypeInDb).all()
        return waste_types
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to get waste types: {str(e)}")
    
@waste_types_router.post("/",response_model=WasteTypeInDb,status_code=status.HTTP_201_CREATED)
async def create_waste_type(waste_type: WasteTypeCreate,db: AsyncSession = Depends(get_db)):
    try:
        new_waste_type = WasteTypeInDb(**waste_type.model_dump())
        db.add(new_waste_type)
        await db.commit()
        await db.refresh(new_waste_type)
        return new_waste_type
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to create waste type: {str(e)}")
    
@waste_types_router.get("/{waste_type_id}",response_model=WasteTypeInDb | None)
async def get_waste_type(waste_type_id: int,db: AsyncSession = Depends(get_db)):
    try:
        waste_type = await db.get(WasteTypeInDb,waste_type_id)
        if waste_type is None:
            raise HTTPException(status_code=404,detail="Waste type not found")
        return waste_type
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to get waste type: {str(e)}")
    
@waste_types_router.put("/{waste_type_id}",response_model=WasteTypeInDb,status_code=status.HTTP_200_OK)
async def update_waste_type(waste_type_id: int,waste_type: WasteTypeUpdate,db: AsyncSession = Depends(get_db)):
    try:
        db_waste_type = await db.get(WasteTypeInDb,waste_type_id)
        if db_waste_type is None:
            raise HTTPException(status_code=404,detail="Waste type not found")
        for key,value in waste_type.model_dump().items():
            setattr(db_waste_type,key,value)
        await db.commit()
        await db.refresh(db_waste_type)
        return db_waste_type
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to update waste type: {str(e)}")
    
@waste_types_router.delete("/{waste_type_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_waste_type(waste_type_id: int,db: AsyncSession = Depends(get_db)):
    try:
        db_waste_type = await db.get(WasteTypeInDb,waste_type_id)
        if db_waste_type is None:
            raise HTTPException(status_code=404,detail="Waste type not found")
        log_entry = LogEntry(
            action="delete",
            entity_type="WasteType",
            entity_id=str(waste_type_id),
            data = db_waste_type.__dict__
        )
        await db.add(log_entry)
        await db.delete(db_waste_type)
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to delete waste type: {str(e)}")
    
@waste_types_router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_waste_types(db: AsyncSession = Depends(get_db)):
    try:
        await db.query(WasteTypeInDb).delete()
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to delete all waste types: {str(e)}")