# Optional: custom pydantic or logic validators
from datetime import datetime

def is_greater_than_zero(value: int):
    if value <= 0:
        raise ValueError(f"{value} is not valid.")
    return value
    
def is_not_null_or_empty(value: str):
    if value is None or value == "":
        raise ValueError(f"{value} is null or empty.")
    return value

def validate_datetime_string(value: str) -> str:
    try:
        datetime.fromisoformat(value)
    except ValueError:
        raise ValueError("Invalid datetime format. Must be ISO 8601 (e.g. '2025-05-19T14:00:00')")
    return value
