from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db, entity_exists
from app.db.models import UserCreate,User
from app.utils.password import hash_password

users_router = APIRouter(prefix="/users")

@users_router.post("/register",status_code=status.HTTP_201_CREATED)
async def register(user:UserCreate,db: AsyncSession = Depends(get_db)):
    if await entity_exists(db,User,email = user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already exists")
    db_user=User(
        email=user.email,
        names=user.names,
        avatar=user.avatar,
        role=user.role,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user