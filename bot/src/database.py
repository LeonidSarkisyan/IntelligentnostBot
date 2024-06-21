import asyncpg

from src.config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME


async def get_connect_with_database() -> asyncpg.connection.Connection:
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        host=DB_HOST
    )
    return conn
