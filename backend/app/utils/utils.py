import bcrypt
from fastapi import HTTPException,Depends,status
from app.auth import Settings, get_current_user
from app.db.models import User
import time
from datetime import timedelta
import jwt
from app.auth import settings

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(10)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password,hashed) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'),hashed.encode('utf-8'))

def role_required(required_roles:list[str]):
    def role_checker(current_user:User = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access denied")
        return current_user
    return role_checker

def create_access_token(subject:str,expires_delta:timedelta = timedelta(minutes=30)) -> str:
    to_encode = {"sub": str(subject),"exp": int(time.time())+ expires_delta.total_seconds()}
    encoded_jwt = jwt.encode(to_encode,settings.ACCESS_TOKEN_SECRET,algorithm="HS256")
    return encoded_jwt