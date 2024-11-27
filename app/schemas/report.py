from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class ReportBase(BaseModel):
    type: str
    time: datetime
    data: str

class ReportCreate(ReportBase):
    pass  # Add fields for creating

class ReportUpdate(ReportBase):
    type: Optional[str] = None
    time: Optional[datetime] = None
    data: Optional[str] = None

class ReportOut(ReportBase):
    id: UUID

    class Config:
        from_attributes = True
