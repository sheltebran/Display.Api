from datetime import timezone
from dateutil.parser import parse
import pytz

def format_date(date_string: str):

    # Ensure it's timezone-aware
    event_date = parse(date_string)

    # Normalize to a proper UTC tzinfo (fixes compatibility with asyncpg/PostgreSQL)
    formatted_date = event_date.astimezone(timezone.utc)

    return formatted_date

def convert_utc_to_pdt(utc_dt):
    """ Convert a UTC datetime to Pacific Daylight Time (PDT). """
    
    # Define the PDT timezone
    pdt_timezone = pytz.timezone('US/Pacific')

    return utc_dt.astimezone(pdt_timezone)
