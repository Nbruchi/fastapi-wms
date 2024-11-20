from typing import AsyncGenerator, Type
from sqlalchemy import exists,select
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

engine = create_async_engine(DATABASE_URL,echo=True)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

async def entity_exists(db: AsyncSession, model: Type[Base], **kwargs) -> bool:
    query = select(exists().where(*[getattr(model,key) == value for key,value in kwargs.items()]))
    result = await db.execute(query)
    return result.scalar()
