import os
import psycopg2 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database_if_not_exists():
    """Create database

    If this database does not exist, then create it
    """
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",  # connect to default DB
        user="postgres",
        password=os.environ["MAIN_DB_PASSWORD"],
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

def create_headline_table():
    """Create the headline table

    Create headlines table setting all column and string sizes
    """    
    conn = psycopg2.connect(
        host="localhost",
        database="displaydb",
        user="test",
        password=os.environ["DB_PASSWORD"],
        port=5432
    )
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

def get_connection():
    """Get database connection

    Returns
    -------
    connection
        Service to enable processing of database calls
    """    
    return psycopg2.connect(
        host="localhost",
        database="displaydb",
        user="test",
        password=os.environ["DB_PASSWORD"],
        port=5432
    )

"""
if __name__ == "__main__":
    create_database_if_not_exists()
create_display_table()
"""
