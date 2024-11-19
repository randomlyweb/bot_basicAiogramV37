import os
from dotenv import load_dotenv
import asyncpg

load_dotenv()

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')
HOST = os.getenv('HOST')


async def init_db():
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    await c.execute('''
    CREATE TABLE IF NOT EXISTS users 
    (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT UNIQUE
    )
    ''')

    await c.close()


async def add_user(telegram_id: int) -> None:
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    await c.execute('INSERT INTO users (telegram_id) VALUES ($1) ON CONFLICT DO NOTHING', telegram_id)

    await c.close()