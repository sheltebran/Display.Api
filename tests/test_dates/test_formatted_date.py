from core.date_helpers import format_date
from datetime import datetime
from datetime import timezone
from core.date_helpers import convert_utc_to_pdt
import pytest
import pytz

@pytest.mark.parametrize("test_date, expected", [
    ("8/24/2017 2:35 PM -07:00", datetime(2017, 8, 24, 21, 35, tzinfo=timezone.utc)),
    ("12/31/2020 11:59 PM -07:00", datetime(2021, 1, 1, 6, 59, tzinfo=timezone.utc)),
    ("1/1/2000 12:00 AM -07:00", datetime(2000, 1, 1, 7, 0, tzinfo=timezone.utc)),
    ("6/15/2022 3:45 PM -07:00", datetime(2022, 6, 15, 22, 45, tzinfo=timezone.utc)),
    ("8/24/2017 2:35 PM +00:00", datetime(2017, 8, 24, 14, 35, tzinfo=timezone.utc))
])

def test_formatted_date(test_date, expected):
    """Test the format_date function with various date formats."""

    # Act
    formatted_date = format_date(test_date)

    # Assert
    assert formatted_date == expected

def test_convert_utc_to_pdt():
    """Test the conversion of UTC datetime to Pacific Daylight Time (PDT)."""
    
    # Arrange
    utc_dt = datetime(2021, 8, 24, 21, 35, tzinfo=timezone.utc)
    
    # Act
    pdt_dt = convert_utc_to_pdt(utc_dt)

    # Assert
    print("\nTesting conversion of UTC datetime to PDT...")
    print(f"Original UTC datetime: {str(utc_dt)}")
    print(f"Converted PDT datetime: {str(pdt_dt)}") 
    assert pdt_dt == utc_dt.astimezone(timezone.utc)

def test_convert_naive_to_pdt_with_non_utc():
    """Test the conversion of a non-UTC datetime to Pacific Daylight Time (PDT)."""
    
    # Arrange
    pdt_timezone = pytz.timezone('US/Pacific')
    naive_dt = datetime(2021, 8, 24, 21, 35)  # naive datetime
    
    # Act
    pdt_dt = convert_utc_to_pdt(naive_dt)

    # Assert
    print("\nTesting conversion of naive datetime to PDT...")
    print(f"Original naive datetime: {str(naive_dt)}")
    print(f"Converted PDT datetime: {str(pdt_dt)}") 
    assert pdt_dt.tzinfo is not None  # Should be timezone-aware after conversion
    assert pdt_dt == naive_dt.astimezone(pdt_timezone) # Ensure it matches the expected PDT time

def test_convert_naive_to_utc_with_non_utc():
    """Test the conversion of a non-UTC datetime to Pacific Daylight Time (PDT)."""
    
    # Arrange
    naive_dt = datetime(2021, 8, 24, 21, 35)  # naive datetime
    
    # Act
    utc_dt = format_date(str(naive_dt))

    # Assert
    print("\nTesting conversion of naive datetime to UTC...")
    print(f"Original naive datetime: {str(naive_dt)}")
    print(f"Converted UTC datetime: {str(utc_dt)}") 
    assert utc_dt.tzinfo is not None  # Should be timezone-aware after conversion
    assert utc_dt == naive_dt.astimezone(timezone.utc) # Ensure it matches the expected UTC time

