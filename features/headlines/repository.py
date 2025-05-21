# DB access layer
from core.database import get_connection
from features.headlines.schemas import HeadlineCreate
from datetime import datetime

async def add_headline(headline: HeadlineCreate):
    """Add new headline

    Add a new headline and return the result of the addition

    Returns
    -------
    new_id: int
        Returns an integer value. If the value is 0
        or less then the operation failed
    """
    conn = get_connection()

    cur = conn.cursor()

    HEADLINE_INSERT = f"INSERT INTO headlines (headline_type, heading, story, link, pub_date) VALUES ({headline.headline_type}, {headline.heading}, {headline.story}, {headline.link}, {datetime.strptime(headline.pub_date, '%m/%d/%y %H:%M:%S')});RETURNING headline_id;"

    cur.execute(HEADLINE_INSERT)
    
    new_id = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return new_id#[1]

def get_all_headlines(number=0):
        
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT headline_id, heading, story, link, pub_date, league_id
        FROM headlines ORDER BY league_id, pub_date
    """)
    
    headline_list = cur.fetchall()
    cur.close()
    conn.close()

    return headline_list