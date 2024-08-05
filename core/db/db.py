import asyncpg
import datetime

from config import HOST, DB_NAME, USER, PASSWORD


async def init_db():
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    await c.execute('''
    CREATE TABLE IF NOT EXISTS users 
    (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT UNIQUE
    )
    ''')

    await c.execute('''
    CREATE TABLE IF NOT EXISTS locations
    (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE,
        link TEXT,
        address TEXT UNIQUE
    )
    ''')

    await c.execute('''
    CREATE TABLE IF NOT EXISTS quizes_name
    (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE,
        link TEXT
    )
    ''')

    await c.execute('''
        CREATE TABLE IF NOT EXISTS categories
        (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE
        )
        ''')

    await c.execute('''
        CREATE TABLE IF NOT EXISTS quizes
        (
            id SERIAL PRIMARY KEY,
            location_id INT REFERENCES locations(id),
            quiz_id INT REFERENCES quizes_name(id),
            quiz_time TIMESTAMP,
            tag TEXT
        )
        ''')

    await c.close()


async def add_user(telegram_id: int) -> None:
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    await c.execute('INSERT INTO users (telegram_id) VALUES ($1) ON CONFLICT DO NOTHING', telegram_id)

    await c.close()


async def select_all_quizes() -> tuple:
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    quizes = await c.fetch('''SELECT * FROM quizes WHERE date_trunc('day', quiz_time) >= date_trunc('day', CURRENT_TIMESTAMP)''')

    await c.close()
    return quizes


async def select_location_by_id(location_id: int) -> str:
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    location = await c.fetch('SELECT name FROM locations WHERE id = $1', location_id)

    await c.close()
    return location


async def select_categories_by_id_quiz_id(quiz_id: id) -> tuple:
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    categories = await c.fetch('SELECT categories_array FROM quizes WHERE id = $1', quiz_id)

    await c.close()
    return categories


async def select_category_name(category_id: int) -> str:
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    name = await c.fetch('SELECT name, id FROM categories WHERE id = $1', category_id)

    await c.close()
    return name


async def select_all_categories() -> dict:
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    categories = await c.fetch('SELECT name, id FROM categories')

    await c.close()
    return categories


async def select_all_rows_with_category(category_id: str) -> dict:
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    rows = await c.fetch('''
    SELECT *
    FROM quizes
    WHERE (categories_array @@ to_tsquery($1)) AND (date_trunc('day', quiz_time) >= date_trunc('day', CURRENT_TIMESTAMP))
    ORDER BY quiz_time ASC
    ''', category_id)

    await c.close()
    return rows


async def select_rows_with_need_date():
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    rows = await c.fetch('''
    SELECT * 
    FROM quizes
    WHERE date_trunc('day', quiz_time) = date_trunc('day', CURRENT_TIMESTAMP)
    ORDER BY quiz_time ASC
    ''')

    await c.close()
    return rows


async def select_rows_for_tomorrow():
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    rows = await c.fetch('''
        SELECT * 
        FROM quizes
        WHERE date_trunc('day', quiz_time) = date_trunc('day', CURRENT_TIMESTAMP) + interval '1 day'
        ORDER BY quiz_time ASC
        ''')

    await c.close()
    return rows


async def select_rows_for_week():
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    rows = await c.fetch('''
    SELECT * 
    FROM quizes
    WHERE date_trunc('day', quiz_time) >= date_trunc('day', CURRENT_TIMESTAMP)
    AND date_trunc('day', quiz_time) <= date_trunc('day', CURRENT_TIMESTAMP) + interval '7 days'
    ORDER BY quiz_time ASC
    ''')

    await c.close()
    return rows


async def select_rows_for_need_day(year, month, day):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    rows = await c.fetch('''
    SELECT * 
    FROM quizes
    WHERE date_trunc('day', quiz_time) = date_trunc('day', $1::date)
    ORDER BY quiz_time ASC
    ''', datetime.date(year=int(year), month=int(month), day=int(day)))

    await c.close()
    return rows


async def select_all_places():
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    rows = await c.fetch('''
    SELECT * 
    FROM locations
    ''')

    await c.close()
    return rows


async def select_all_quizes_for_location(location_id: int):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    rows = await c.fetch('''
    SELECT * 
    FROM quizes 
    WHERE (location_id = $1) AND (date_trunc('day', quiz_time) >= date_trunc('day', CURRENT_TIMESTAMP))
    ORDER BY quiz_time ASC
    ''', location_id)
    await c.close()
    return rows


async def select_quiz_name_by_id(quiz_id: int):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    rows = await c.fetch('''
    SELECT name, id 
    FROM quizes_name 
    WHERE id = $1
    ''', quiz_id)

    await c.close()
    return rows


async def select_all_quizes_():
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    rows = await c.fetch('''
    SELECT name, id, link 
    FROM quizes_name
    ''')
    await c.close()
    return rows


async def select_all_quizes_for_quiz(quiz_id: int):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    rows = await c.fetch('''
    SELECT * 
    FROM quizes
    WHERE (quiz_id = $1) AND (date_trunc('day', quiz_time) >= date_trunc('day', CURRENT_TIMESTAMP)) 
    ORDER BY quiz_time ASC
    ''', quiz_id)

    await c.close()
    return rows


# async def select_category_name_by_id(category_id: int):
#     c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)
#
#     rows = await c.fetch('''
#     SELECT name, id
#     FROM categories
#     WHERE id = $1
#     ''', category_id)
#
#     await c.close()
#     return rows


async def select_all_locations():
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    rows = await c.fetch('''
    SELECT name, id, link, address
    FROM locations
    ''')
    await c.close()
    return rows


# ADMIN FUNCTIONS
async def add_location_if_not_exists(location_name: str, link: str, address: str):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    await c.execute('''
    INSERT INTO locations
    (name, link, address)
    VALUES
    ($1, $2, $3)
    ON CONFLICT DO NOTHING
    ''', location_name, link, address)

    await c.close()


async def add_quiz_if_not_exists(quiz_name: str, quiz_link: str):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    await c.execute('''
    INSERT INTO quizes_name
    (name, link)
    VALUES
    ($1, $2)
    ON CONFLICT DO NOTHING
    ''', quiz_name, quiz_link)

    await c.close()


async def add_category_if_not_exists(category_name: str):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    await c.execute('''
    INSERT INTO categories
    (name)
    VALUES
    ($1)
    ''', category_name)

    await c.close()


async def select_quiz_name_by_name(quiz_name: str):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    rows = await c.fetch('''
    SELECT id, name 
    FROM quizes_name
    WHERE name ILIKE $1
    ''', quiz_name)

    await c.close()
    return rows


async def select_location_name_by_name(location_name: str):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    rows = await c.fetch('''
    SELECT id, name 
    FROM locations
    WHERE name ILIKE $1
    ''', location_name)

    await c.close()
    return rows


# async def select_thematic_name_by_name(category_name: str):
#     c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)
#
#     rows = await c.fetch('''
#     SELECT id, name
#     FROM categories
#     WHERE name ILIKE $1
#     ''', category_name)
#
#     await c.close()
#     return rows


async def add_quiz(location_id: int, quiz_id: int, year: int, month: int, day: int, hours :int, minutes: int, tag: str):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    await c.execute('''
    INSERT INTO quizes
    (location_id, quiz_id, quiz_time, tag)
    VALUES
    ($1, $2, $3, $4)
    ''', location_id, quiz_id, datetime.datetime(year=year, month=month, day=day, hour=hours, minute=minutes, second=0), tag)

    await c.close()


async def check_for_quiz(location_id: int, quiz_id: int, year: int, month: int, day: int, hours :int, minutes: int, tag: str):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    row = await c.fetch('''
    SELECT * 
    FROM quizes 
    WHERE (location_id = $1) AND (quiz_id = $2) AND (tag = $3)''',
                        location_id, quiz_id, tag)
    if row == []:
        return False
    else:
        return True


async def edit_quiz(quiz_id: int, new_quiz_name: str, link: str):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    await c.execute('''
    UPDATE quizes_name
    SET (name, link) = ($1, $2)
    WHERE id = $3
    ''', new_quiz_name, link, int(quiz_id))

    await c.close()


async def edit_location(location_id: int, new_location_name: str, link: str, address: str):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    await c.execute('''
    UPDATE locations
    SET (name, link, address) = ($1, $2, $3)
    WHERE id = $4
    ''',
                    new_location_name, link, address, location_id)


async def delete_quiz_name(quiz_id: int):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    await c.execute('''
    DELETE
    FROM quizes
    WHERE quiz_id = $1
    ''', quiz_id)

    await c.execute('''
    DELETE
    FROM quizes_name
    WHERE id = $1
    ''', quiz_id)

    await c.close()


async def delete_location(location_id: int):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    await c.execute('''
    DELETE
    FROM quizes
    WHERE location_id = $1
    ''', location_id)

    await c.execute('''
    DELETE
    FROM locations
    WHERE id = $1
    ''', location_id)

    await c.close()


async def select_all_quizes___():
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    rows = await c.fetch('''
    SELECT * 
    FROM quizes 
    WHERE date_trunc('day', quiz_time) >= date_trunc('day', CURRENT_TIMESTAMP)
    ORDER BY quiz_time ASC
    ''')
    await c.close()
    return rows


async def select_quiz_by_id(quiz_id: int):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    rows = await c.fetch('''
    SELECT * 
    FROM quizes
    WHERE id = $1
    ''', quiz_id)

    await c.close()
    return rows


async def delete_quiz(quiz_id: int):
    c = await asyncpg.connect(user=USER, password=PASSWORD, database=DB_NAME, host=HOST)

    await c.execute('''
    DELETE
    FROM quizes
    WHERE id = $1
    ''', quiz_id)

    await c.close()