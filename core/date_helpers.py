from datetime import timezone
from dateutil.parser import parse

def format_date(date_string: str):

    # Ensure it's timezone-aware
    event_date = parse(date_string)

    # Normalize to a proper UTC tzinfo (fixes compatibility with asyncpg/PostgreSQL)
    formatted_date = event_date.astimezone(timezone.utc)

    return formatted_date