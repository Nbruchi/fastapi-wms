from datetime import datetime
from pydantic import BaseModel,Field
from sqlalchemy import Column, Integer, String, DateTime,JSON,Enum,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from typing import Optional
from fastapi_users import schemas
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

Base = declarative_base()

class LoginRequest(BaseModel):
    email: str
    password: str

class UserRole(PyEnum):
    admin = "admin"
    staff = "staff"
    user = "user"

class UserRead(schemas.BaseUser):
    names: str
    email:str
    avatar: Optional[str] = None
    role: UserRole = UserRole.user

class UserCreate(schemas.BaseUserCreate):
    names: str
    email:str
    avatar: Optional[str] = None
    role: UserRole = UserRole.user
    password: str = Field(..., min_length=8)

class UserUpdate(schemas.BaseUserUpdate):
    names: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    role: Optional[UserRole] = UserRole.user

class User(SQLAlchemyBaseUserTableUUID,Base):
    __tablename__ = "users"
    names = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    avatar = Column(String,nullable=True)
    role = Column(Enum(UserRole),nullable=False,default=UserRole.user)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),server_default=func.now(), onupdate=func.now())

class LogEntry(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True,index=True)
    action = Column(String)
    entity_type = Column(String)
    entity_id = Column(String)
    timestamp = Column(DateTime,default=datetime.now())
    data = Column(JSON)

class WasteTypeBase(BaseModel):
    name: str
    code: Optional[int] = None

class WasteTypeCreate(WasteTypeBase):
    pass

class WasteTypeUpdate(WasteTypeBase):
    pass

class WasteTypeInDb(WasteTypeBase):
    id: int
    name: str
    code: int
    created_at: datetime

    class Config:
        from_attributes = True

class WasteType(Base):
    __tablename__ = "waste_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(Integer, nullable=True)
    
    # Timestamp fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CollectionPointBase(BaseModel):
    name: str
    address: str

class CollectionPointCreate(CollectionPointBase):
    pass

class CollectionPointUpdate(CollectionPointBase):
    pass

class CollectionPointInDb(CollectionPointBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
    
class CollectionPoint(Base):
    __tablename__ = "collection_points"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    
    # Timestamp fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),server_default=func.now(), onupdate=func.now())

class CollectionScheduleBase(BaseModel):
    collection_point_id: int
    waste_type_id: int
    schedule: str
    start_date: str
    end_date: str

class CollectionScheduleCreate(CollectionScheduleBase):
    pass

class CollectionScheduleUpdate(CollectionScheduleBase):
    pass

class CollectionScheduleInDb(CollectionScheduleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
    
class CollectionSchedule(Base):
    __tablename__ = "collection_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    collection_point_id = Column(Integer, nullable=False)
    waste_type_id = Column(Integer, nullable=False)
    schedule = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    
    # Timestamp fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),server_default=func.now(), onupdate=func.now())

class CollectionRecordBase(BaseModel):
    collection_schedule_id: int
    collection_date: str
    quantity_collected: int
    recycle_rate: float

class CollectionRecordCreate(CollectionRecordBase):
    pass

class CollectionRecordUpdate(CollectionRecordBase):
    pass

class CollectionRecordInDb(CollectionRecordBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CollectionRecord(Base):
    __tablename__ = "collection_records"
    
    id = Column(Integer, primary_key=True, index=True)
    collection_schedule_id = Column(Integer, nullable=False)
    collection_date = Column(String, nullable=False)
    quantity_collected = Column(Integer, nullable=False)
    recycle_rate = Column(Float, nullable=False)
    
    # Timestamp fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),server_default=func.now(), onupdate=func.now())