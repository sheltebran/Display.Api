from core.date_helpers import format_date
from datetime import datetime
from datetime import timezone
import pytest

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
