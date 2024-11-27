import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from app.database import Base  # Import your combined Base

# Load Alembic config
config = context.config

# Interpret the config file for Python logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# Set target metadata for migrations
target_metadata = Base.metadata

# Define your database URL
DATABASE_URL = "postgresql+asyncpg://bruce:bruce@localhost/fastapi"

# Async function to run migrations
async def run_async_migrations():
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

# Synchronous wrapper for running migrations
def run_migrations_online():
    asyncio.run(run_async_migrations())

# Core migration logic
def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()

# Call the async wrapper
run_migrations_online()
