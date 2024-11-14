from datetime import datetime
from pydantic import BaseModel,Field
from sqlalchemy import Column, Integer, String, DateTime,JSON,Enum
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum
from fastapi_users import schemas
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

Base = declarative_base()

class UserRole(PyEnum):
    admin = "admin"
    staff = "staff"
    user = "user"

class UserRead(schemas.BaseUser):
    names: str
    email:str
    avatar: str | None = None
    role: UserRole = UserRole.user

class UserCreate(schemas.BaseUserCreate):
    names: str
    email:str
    avatar: str | None = None
    role: UserRole = UserRole.user
    password = str = Field(..., min_length=8)

class UserUpdate(schemas.BaseUserUpdate):
    names: str
    email:str
    avatar: str | None = None
    role: UserRole = UserRole.user

class User(SQLAlchemyBaseUserTableUUID,Base):
    __tablename__ = "users"
    names = Column(String,nullable=False)
    avatar = Column(String,nullable=True)
    role = Column(Enum(UserRole),nullable=False,default=UserRole.user)

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
    recycling_code: str | None = None

class WasteTypeCreate(WasteTypeBase):
    pass

class WasteTypeUpdate(WasteTypeBase):
    pass

class WasteTypeInDb(WasteTypeBase):
    id: int

    class Config:
        from_attributes = True

class CollectionPointBase(BaseModel):
    name: str
    address: str

class CollectionPointCreate(CollectionPointBase):
    pass

class CollectionPointUpdate(CollectionPointBase):
    pass

class CollectionPointInDb(CollectionPointBase):
    id: int

    class Config:
        from_attributes = True

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

    class Config:
        from_attributes = True

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

    class Config:
        from_attributes = True