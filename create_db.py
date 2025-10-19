import asyncio
import json
import os
from urllib.parse import urlparse, urlunparse

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


async def drop_and_create_async_db(database_url: str):
    """
    Asynchronously drops and recreates a PostgreSQL database.
    """
    # 1. Parse the original URL to connect to the default 'postgres' database
    parsed_url = urlparse(database_url)
    db_name = parsed_url.path.lstrip('/')
    
    # Create a URL for the maintenance database (postgres)
    maintenance_url_parts = parsed_url._replace(path="/postgres")
    maintenance_url = urlunparse(maintenance_url_parts)
    
    # 2. Create an engine to the maintenance database
    engine = create_async_engine(maintenance_url, isolation_level="AUTOCOMMIT")

    # 3. Connect and execute raw SQL commands
    async with engine.connect() as conn:
        await conn.execute(text(f'DROP DATABASE IF EXISTS "{db_name}"'))
        print(f"Database '{db_name}' dropped.")
            
        print(f"Creating database: '{db_name}'")
        await conn.execute(text(f'CREATE DATABASE "{db_name}"'))
        print("Database created successfully.")

    await engine.dispose()


    

if __name__ == "__main__":
    DB_URL = os.getenv("DATABASE_URL")
    if not DB_URL:
        raise ValueError("DATABASE_URL environment variable not set.")
        
    asyncio.run(drop_and_create_async_db(DB_URL))
    asyncio.run(seed_db())