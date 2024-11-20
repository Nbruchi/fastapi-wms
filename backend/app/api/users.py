from fastapi import APIRouter,Depends,status,HTTPException,Response,Body
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db, entity_exists
from app.db.models import LoginRequest, UserCreate,User, UserRead,UserUpdate
from app.utils.utils import create_access_token, hash_password, verify_password

users_router = APIRouter(prefix="/users")

@users_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Check if user already exists
        if await entity_exists(db, User, email=user.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        
        # Create a new user object
        db_user = User(
            email=user.email,
            names=user.names,
            avatar=user.avatar,
            role=user.role,
            hashed_password=hash_password(user.password)
        )
        
        # Add the user to the database
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@users_router.post("/login",status_code=status.HTTP_200_OK)
async def login(request:LoginRequest,db:AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).where(User.email == request.email))
        user = result.scalar_one_or_none()

        if not user or not verify_password(request.password,user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        access_token = create_access_token(subject=user.id)
        return {"access_token":access_token,"token_type":"bearer"}
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@users_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    try:
        # Clear the Authorization cookie
        response.delete_cookie(key="Authorization", path="/", httponly=True)
        return {"message": "Successfully logged out"}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to log out")


@users_router.get("/",response_model=list[UserRead],status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User))
        users = result.scalars().all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to get users: {str(e)}")

@users_router.get("/{user_id}",response_model=UserRead,status_code=status.HTTP_200_OK)
async def get_user(user_id: str,db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
        return user    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to get user: {str(e)}")

@users_router.put("/{user_id}",response_model=UserRead,status_code=status.HTTP_200_OK)
async def update_user(user_id: str,user_update: UserUpdate,db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        db_user = result.scalar()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
        for key,value in user_update.model_dump(exclude={"password"},exclude_unset=True).items():
            setattr(db_user,key,value)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to update user: {str(e)}")

@users_router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str,db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        db_user = result.scalar()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
        await db.delete(db_user)
        await db.commit()
        return {"message":f"User with id {user_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to delete user: {str(e)}")

@users_router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_users(db: AsyncSession = Depends(get_db)):
    try:
        statement = delete(User)
        await db.execute(statement)
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to delete all users: {str(e)}")