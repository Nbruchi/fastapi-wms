from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import text  # Import the text construct for raw SQL queries

# Database URL
DATABASE_URL = "postgresql+asyncpg://bruce:bruce@localhost/fastapi"

# Create a unified declarative base
Base = declarative_base()

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True enables query logging

# Define the async session factory
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency to provide a session
async def get_db():
    async with async_session() as session:
        yield session

# Test the database connection
async def test_connection():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))  # Use `text` for raw SQL
            print("🟢 Database connected successfully.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise e  # Re-raise the exception for further debugging
