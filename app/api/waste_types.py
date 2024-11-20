from app.db.database import get_db
from sqlalchemy import exists,delete
from sqlalchemy.future import select
from app.auth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, UserRole, WasteType
from fastapi import APIRouter, Depends, HTTPException,status
from app.db.models import (LogEntry, WasteTypeCreate,WasteTypeUpdate,WasteTypeInDb)

waste_types_router = APIRouter(prefix="/waste-types")

async def waste_type_exists(db:AsyncSession = Depends(get_db),waste_type_id:int = None) -> bool:
    result = await db.execute(select(exists().where(WasteTypeInDb.id == waste_type_id)))
    return result.scalar()

@waste_types_router.get("/",response_model=list[WasteTypeInDb],status_code=status.HTTP_200_OK)
async def get_waste_types(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(WasteType))
        waste_types = result.scalars().all()
        return waste_types
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to get waste types: {str(e)}")
    
@waste_types_router.post("/",response_model=WasteTypeInDb,status_code=status.HTTP_201_CREATED)
async def create_waste_type(
    waste_type: WasteTypeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
        new_waste_type = WasteType(
            name = waste_type.name,
            code = waste_type.code
        )
        db.add(new_waste_type)
        await db.commit()
        await db.refresh(new_waste_type)
        return new_waste_type
    except Exception as e:
        print(f"Creation error: {str(e)}")
        raise HTTPException(status_code=500,detail=f"Failed to create waste type: {str(e)}")
    
@waste_types_router.get("/{waste_type_id}",response_model=WasteTypeInDb | None)
async def get_waste_type(
    waste_type_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await db.execute(select(WasteType).where(WasteType.id == waste_type_id))
        waste_type = result.scalar()
        if waste_type is None:
            raise HTTPException(status_code=404,detail="Waste type not found")
        return waste_type
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to get waste type: {str(e)}")
    
@waste_types_router.put("/{waste_type_id}", response_model=WasteTypeInDb, status_code=status.HTTP_200_OK)
async def update_waste_type(
    waste_type_id: int,
    waste_type: WasteTypeUpdate,  # This is the input Pydantic model
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

        # Query to find the WasteType instance
        result = await db.execute(select(WasteType).where(WasteType.id == waste_type_id))
        db_waste_type = result.scalar()  # Extract the actual object, not the result wrapper

        if db_waste_type is None:
            raise HTTPException(status_code=404, detail="Waste type not found")

        # Update the waste type attributes from the input Pydantic model
        for key, value in waste_type.model_dump(exclude_unset=True).items():
            setattr(db_waste_type, key, value)

        # Commit changes to the database
        await db.commit()
        await db.refresh(db_waste_type)

        return db_waste_type
    except Exception as e:
        await db.rollback()
        print(f"Updation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update waste type: {str(e)}")

    
@waste_types_router.delete("/{waste_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_waste_type(
    waste_type_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Check if the user is an admin
        if current_user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

        # Query the waste type object
        result = await db.execute(select(WasteType).where(WasteType.id == waste_type_id))
        db_waste_type = result.scalar()

        # If the waste type doesn't exist, return a 404
        if db_waste_type is None:
            raise HTTPException(status_code=404, detail="Waste type not found")

        # Log the action before deletion
        log_entry = LogEntry(
            action="delete",
            entity_type="WasteType",
            entity_id=str(waste_type_id),
            data=db_waste_type.__dict__  # Capture the model's dictionary for logging
        )

        await db.add(log_entry)

        # Proceed with deletion
        await db.delete(db_waste_type)  # Delete the waste type object
        await db.commit()  # Commit the transaction to apply the changes
    except Exception as e:
        await db.rollback()  # In case of error, ensure to rollback
        raise HTTPException(status_code=500, detail=f"Failed to delete waste type: {str(e)}")
    
@waste_types_router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_waste_types(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
        statement = delete(WasteType)
        await db.execute(statement)
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to delete all waste types: {str(e)}")