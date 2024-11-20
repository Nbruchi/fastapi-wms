import jwt
from app.db.models import User
from app.db.database import get_db
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users import FastAPIUsers
from pydantic_settings import BaseSettings
from fastapi import Request,HTTPException,status,Depends
from fastapi_users.authentication import JWTStrategy,AuthenticationBackend,BearerTransport

bearer_transport = BearerTransport(tokenUrl="auth/login")

class Settings(BaseSettings):
    ACCESS_TOKEN_SECRET: str
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.ACCESS_TOKEN_SECRET, lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)

fastapi_users = FastAPIUsers(get_jwt_strategy,auth_backend)

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> User:
    try:
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
        
        token = token.split(" ")[1]  # Extract the token part of the Authorization header
        payload = jwt.decode(token, settings.ACCESS_TOKEN_SECRET, algorithms=["HS256"])
        
        user_id = payload.get("sub")  # This assumes 'sub' contains the user ID
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: sub not found")
        
        # Fetch user from the database using the decoded user_id
        user = await db.execute(select(User).where(User.id == user_id))
        user = user.scalar_one_or_none()  # Use scalar_one_or_none to get a single result or None
        
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")