from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class RecycleBase(BaseModel):
    type: str
    quantity: float
    date: datetime
    schedule_id: UUID  # Include schedule_id as part of the model

class RecycleCreate(RecycleBase):
    pass  # Add fields for creating (no need for id)

class RecycleUpdate(RecycleBase):
    type: Optional[str] = None
    quantity: Optional[float] = None
    date: Optional[datetime] = None
    schedule_id: Optional[UUID] = None  # Allow for updating the schedule_id

class RecycleOut(RecycleBase):
    id: UUID

    class Config:
        from_attributes = True
