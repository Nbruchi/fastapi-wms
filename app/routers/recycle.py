from typing import List
from fastapi import APIRouter, Depends, HTTPException,status,Query
from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.recycle import Recycle
from app.services.recycle import create_recycle, get_recycles, get_recycle, update_recycle, delete_recycle,get_paginated_recycles
from app.schemas.recycle import RecycleCreate, RecycleUpdate, RecycleOut
from app.database import get_db
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=RecycleOut)
async def create_recycle_endpoint(recycle: RecycleCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_recycle(db, recycle)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))



@router.get("/", response_model=List[RecycleOut])
async def read_recycles(db: AsyncSession = Depends(get_db)):
    try:
        recycles = await get_recycles(db)
        return recycles
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))




@router.get("/all", response_model=dict)
async def read_paginated_recycles(skip: int = 0, limit: int = 50,db:AsyncSession = Depends(get_db)) -> dict:
    try:
        total_query = await db.execute(select(func.count(Recycle.id)))
        total_items = total_query.scalar_one()
        recycles = await get_paginated_recycles(db,skip=skip,limit=limit)
        return {"recycles": recycles, "total": total_items}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))



@router.get("/{recycle_id}", response_model=RecycleOut)
async def read_recycle(recycle_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        db_recycle = await get_recycle(db, recycle_id)
        if db_recycle is None:
            raise HTTPException(status_code=404, detail="Recycling log not found")
        return db_recycle
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))



@router.put("/{recycle_id}", response_model=RecycleOut)
async def update_recycle_endpoint(recycle_id: UUID, recycle_update: RecycleUpdate, db: AsyncSession = Depends(get_db)):
    try:
        db_recycle = await update_recycle(db, recycle_id, recycle_update)
        if db_recycle is None:
            raise HTTPException(status_code=404, detail="Recycling log not found")
        return db_recycle
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))



@router.delete("/{recycle_id}", response_model=RecycleOut)
async def delete_recycle_endpoint(recycle_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        db_recycle = await delete_recycle(db, recycle_id)
        if db_recycle is None:
            raise HTTPException(status_code=404, detail="Recycling log not found")
        return db_recycle
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
