import os
import asyncpg
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

async def initialize_database():
    await create_database_if_not_exists()
    await create_headlines_table_if_not_exists()
    await create_created_default_picks_table_if_not_exists()
    await create_created_leagues_table_if_not_exists()
    await create_created_user_teams_table_if_not_exists()
    await create_created_weeks_table_if_not_exists()

def get_db_config():
    """Get database connection

    Returns
    -------
    connection
        Service to enable processing of database calls
    """    

    return {
        "host": "localhost",
        "database": "display_db",
        "user": "test",
        "password": os.environ.get("DB_PASSWORD"),
        "port": 5432
    }

async def create_database_if_not_exists():
    """Create database

    If this database does not exist, then create it
    """

    conn = await asyncpg.connect(
        host="localhost",
        database="postgres",  # connect to default DB
        user="postgres",
        password=os.environ.get("MAIN_DB_PASSWORD"),
        port=5432
    )

    # conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # Required for CREATE DATABASE

    command = "SELECT 1 FROM pg_database WHERE datname = 'display_db'"
    exists = await conn.execute(command)

    # If database does not exist, create it
    if not exists:
        await conn.execute("CREATE DATABASE display_db OWNER test")

    await conn.close()

async def create_created_default_picks_table_if_not_exists():
    """Create the created_default_picks table"""

    config = get_db_config()

    try:
        # Connect to the database
        conn = await asyncpg.connect(**config)

        command = """
            CREATE TABLE IF NOT EXISTS created_default_picks (
                created_default_pick_id SERIAL PRIMARY KEY,
                game_id INT NOT NULL,
                favorite_team_id VARCHAR(5) NOT NULL,
                favorite_team_name VARCHAR(100) NOT NULL,
                spread FLOAT NOT NULL,
                week_id INT NOT NULL,
                week_number INT NOT NULL,
                event_date TIMESTAMPTZ NOT NULL);
        """

        await conn.execute(command)

        await conn.close()

    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")

async def create_headlines_table_if_not_exists():
    """Create the headlines table""" 

    config = get_db_config()

    try:
        # Connect to the database
        conn = await asyncpg.connect(**config)

        command = """
            CREATE TABLE IF NOT EXISTS headlines (
                headline_id SERIAL PRIMARY KEY,
                heading VARCHAR(200) NOT NULL,
                story VARCHAR(500) NOT NULL,
                link VARCHAR(500) NOT NULL,
                pub_date TIMESTAMPTZ NOT NULL,
                league_id INT);
        """

        await conn.execute(command)

        await conn.close()

    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
      
async def create_created_weeks_table_if_not_exists() -> None:
    """Create the created_weeks table"""

    config = get_db_config()

    try:
        # Connect to the database
        conn = await asyncpg.connect(**config)

        command = """
            CREATE TABLE IF NOT EXISTS created_weeks (
                created_week_id SERIAL PRIMARY KEY,
                week_id INT NOT NULL,
                week_number INT NOT NULL,
                start_date TIMESTAMPTZ NOT NULL,
                end_date TIMESTAMPTZ NOT NULL,
                deadline_date TIMESTAMPTZ NOT NULL,
                season_id UUID NOT NULL,
                event_date TIMESTAMPTZ NOT NULL);
        """

        await conn.execute(command)

        await conn.close()

    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")

async def create_created_leagues_table_if_not_exists():
    """Create the created_leagues table"""
        
    config = get_db_config()

    try:
        # Connect to the database
        conn = await asyncpg.connect(**config)

        command = """
            CREATE TABLE IF NOT EXISTS created_leagues (
                created_league_id SERIAL PRIMARY KEY,
                league_id int,
                name VARCHAR(50) NOT NULL,
                url VARCHAR(500) NOT NULL,
                sport_id int,
                event_date TIMESTAMPTZ NOT NULL);
        """

        await conn.execute(command)

        await conn.close()

    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")

async def create_created_user_teams_table_if_not_exists():
    """Create the created_user_teams table"""
        
    config = get_db_config()
    
    try:
        # Connect to the database
        conn = await asyncpg.connect(**config)

        command = """
            CREATE TABLE IF NOT EXISTS created_user_teams (
                created_user_team_id SERIAL PRIMARY KEY,
                user_team_id UUID NOT NULL,
                name VARCHAR(100) NOT NULL,
                starting_amount INT NOT NULL,
                is_paid BOOLEAN NOT NULL DEFAULT FALSE,
                payment_reference VARCHAR(50) NULL,
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                slogan VARCHAR(100) NULL,
                email VARCHAR(100) NOT NULL,
                season_id UUID NOT NULL,
                user_id UUID NOT NULL,
                event_date TIMESTAMPTZ NOT NULL);
        """

        await conn.execute(command)

        await conn.close()

    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")

