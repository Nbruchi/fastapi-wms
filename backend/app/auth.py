from fastapi_users.authentication import JWTStrategy,AuthenticationBackend
from fastapi_users import FastAPIUsers
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=None,
    get_strategy=get_jwt_strategy
)

fastapi_users = FastAPIUsers(get_jwt_strategy,auth_backend)