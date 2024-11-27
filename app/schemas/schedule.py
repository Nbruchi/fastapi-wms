from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from uuid import UUID

class ScheduleBase(BaseModel):
    day: str
    time: datetime
    frequency: str

class ScheduleCreate(ScheduleBase):
    pass  # Add fields for creating

class ScheduleUpdate(ScheduleBase):
    day: Optional[str] = None
    time: Optional[datetime] = None
    frequency: Optional[str] = None

class ScheduleOut(ScheduleBase):
    id: UUID

    class Config:
        from_attributes = True
