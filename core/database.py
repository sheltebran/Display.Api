import os
import psycopg2 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# from starlette.concurrency import run_in_threadpool



async def initialize_database():
    await create_database_if_not_exists()
    await create_headlines_table_if_not_exists()
    await create_created_sports_table_if_not_exists()
    await create_created_leagues_table_if_not_exists()

def get_db_config():
    """Get database connection

    Returns
    -------
    connection
        Service to enable processing of database calls
    """    

    return {
        "host": "localhost",
        "dbname": "displaydb",
        "user": "test",
        "password": os.environ.get("DB_PASSWORD"),
        "port": 5432
    }

async def create_database_if_not_exists():
    """Create database

    If this database does not exist, then create it
    """

    pwd = os.environ.get("MAIN_DB_PASSWORD")

    conn = psycopg2.connect(
        host="localhost",
        dbname="postgres",  # connect to default DB
        user="postgres",
        password=pwd,
        port=5432
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # Required for CREATE DATABASE
    cur = conn.cursor()

    # Check if database exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'displaydb'")
    exists = cur.fetchone()

    if not exists:
        cur.execute("CREATE DATABASE displaydb OWNER test")

    cur.close()
    conn.close()

async def create_headlines_table_if_not_exists():
    """Create the headlines table

    Create headlines table setting all column and string sizes
    """    
    config = get_db_config()

    with psycopg2.connect(**config) as conn:
        conn.autocommit = True
        cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS headlines (
            headline_id SERIAL PRIMARY KEY,
            heading VARCHAR(200) NOT NULL,
            story VARCHAR(500) NOT NULL,
            link VARCHAR(500) NOT NULL,
            pub_date TIMESTAMP NOT NULL,
            league_id INT
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

async def create_created_sports_table_if_not_exists() -> None:
        
    config = get_db_config()
    
    with psycopg2.connect(**config) as conn:
        conn.autocommit = True
        cur = conn.cursor()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS created_sports (
            created_sport_id SERIAL PRIMARY KEY,
            sport_id int,
            name VARCHAR(100) NOT NULL,
            event_date TIMESTAMP NOT NULL);""")

    conn.commit()
    cur.close()
    conn.close()

async def create_created_leagues_table_if_not_exists():
        
    config = get_db_config()
    
    with psycopg2.connect(**config) as conn:
        conn.autocommit = True
        cur = conn.cursor()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS created_leagues (
            created_league_id SERIAL PRIMARY KEY,
            league_id int,
            name VARCHAR(50) NOT NULL,
            url VARCHAR(500) NOT NULL,
            sport_id int,
            event_date TIMESTAMP NOT NULL);""")

    conn.commit()
    cur.close()
    conn.close()
