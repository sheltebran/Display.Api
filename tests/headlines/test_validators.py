import pytest
from features.headlines.validators import (
    is_greater_than_zero,
    is_not_null_or_empty,
    validate_datetime_string
)

class TestIsGreaterThanZero:
    """Test cases for is_greater_than_zero validator"""
    
    def test_positive_integer(self):
        """Test validator with positive integer"""
        # Act & Assert
        assert is_greater_than_zero(1) == 1
        assert is_greater_than_zero(100) == 100
        assert is_greater_than_zero(999999) == 999999
    
    def test_zero_value(self):
        """Test validator with zero value"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            is_greater_than_zero(0)
        assert "0 is not valid" in str(exc_info.value)
    
    def test_negative_integer(self):
        """Test validator with negative integer"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            is_greater_than_zero(-1)
        assert "-1 is not valid" in str(exc_info.value)
        
        with pytest.raises(ValueError) as exc_info:
            is_greater_than_zero(-100)
        assert "-100 is not valid" in str(exc_info.value)
    
    def test_large_negative_integer(self):
        """Test validator with very large negative integer"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            is_greater_than_zero(-999999)
        assert "-999999 is not valid" in str(exc_info.value)

class TestIsNotNullOrEmpty:
    """Test cases for is_not_null_or_empty validator"""
    
    def test_valid_string(self):
        """Test validator with valid non-empty string"""
        # Act & Assert
        assert is_not_null_or_empty("test") == "test"
        assert is_not_null_or_empty("Hello World") == "Hello World"
        assert is_not_null_or_empty("123") == "123"
        assert is_not_null_or_empty("   spaces   ") == "   spaces   "
    
    def test_empty_string(self):
        """Test validator with empty string"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            is_not_null_or_empty("")
        assert " is null or empty" in str(exc_info.value)
    
    def test_none_value(self):
        """Test validator with None value"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            is_not_null_or_empty(None)
        assert "None is null or empty" in str(exc_info.value)
    
    def test_whitespace_only_string(self):
        """Test validator with whitespace-only string (should be valid)"""
        # Act & Assert
        assert is_not_null_or_empty("   ") == "   "
        assert is_not_null_or_empty("\t") == "\t"
        assert is_not_null_or_empty("\n") == "\n"
    
    def test_special_characters(self):
        """Test validator with special characters"""
        # Act & Assert
        assert is_not_null_or_empty("!@#$%^&*()") == "!@#$%^&*()"
        assert is_not_null_or_empty("émojis 🏈") == "émojis 🏈"
        assert is_not_null_or_empty("ñoño") == "ñoño"

class TestValidateDatetimeString:
    """Test cases for validate_datetime_string validator"""
    
    def test_valid_iso_format(self):
        """Test validator with valid ISO 8601 datetime strings"""
        # Act & Assert
        valid_dates = [
            "2025-05-19T14:00:00",
            "2024-01-01T00:00:00",
            "2024-12-31T23:59:59",
            "2024-06-15T12:30:45"
        ]
        
        for date_str in valid_dates:
            assert validate_datetime_string(date_str) == date_str
    
    def test_valid_iso_format_with_timezone(self):
        """Test validator with valid ISO 8601 datetime strings with timezone"""
        # Act & Assert
        valid_dates_with_tz = [
            "2025-05-19T14:00:00+00:00",
            "2024-01-01T00:00:00Z",
            "2024-12-31T23:59:59-05:00",
            "2024-06-15T12:30:45+02:00"
        ]
        
        for date_str in valid_dates_with_tz:
            assert validate_datetime_string(date_str) == date_str
    
    def test_valid_iso_format_with_microseconds(self):
        """Test validator with valid ISO 8601 datetime strings with microseconds"""
        # Act & Assert
        valid_dates_with_microseconds = [
            "2025-05-19T14:00:00.123456",
            "2024-01-01T00:00:00.000000",
            "2024-12-31T23:59:59.999999"
        ]
        
        for date_str in valid_dates_with_microseconds:
            assert validate_datetime_string(date_str) == date_str
    
    def test_invalid_date_format(self):
        """Test validator with invalid date formats"""
        # Act & Assert
        invalid_dates = [
            "2024-13-01T12:00:00",  # Invalid month
            "2024-01-32T12:00:00",  # Invalid day
            "2024-01-01T25:00:00",  # Invalid hour
            "2024-01-01T12:60:00",  # Invalid minute
            "2024-01-01T12:00:60",  # Invalid second
        ]
        
        for date_str in invalid_dates:
            with pytest.raises(ValueError) as exc_info:
                validate_datetime_string(date_str)
            assert "Invalid datetime format" in str(exc_info.value)
            assert "Must be ISO 8601" in str(exc_info.value)
    
    def test_invalid_string_format(self):
        """Test validator with completely invalid string formats"""
        # Act & Assert
        invalid_formats = [
            "not a date",
            "01/01/2024",  # US format
            "01-01-2024",  # Different separator
            "2024/01/01",  # Different format
            "January 1, 2024",  # Text format
            "14:00:00",  # Time only, no date
            "",  # Empty string
        ]
        
        for date_str in invalid_formats:
            with pytest.raises(ValueError) as exc_info:
                validate_datetime_string(date_str)
            assert "Invalid datetime format" in str(exc_info.value)
    
    def test_none_value(self):
        """Test validator with None value"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            validate_datetime_string(None)
        assert "Invalid datetime format" in str(exc_info.value)
    
    def test_edge_case_dates(self):
        """Test validator with edge case valid dates"""
        # Act & Assert
        edge_cases = [
            "2000-02-29T12:00:00",  # Leap year
            "1900-01-01T00:00:00",  # Old date
            "2099-12-31T23:59:59",  # Future date
            "2024-02-29T12:00:00",  # Leap year 2024
        ]
        
        for date_str in edge_cases:
            assert validate_datetime_string(date_str) == date_str
    
    def test_invalid_leap_year(self):
        """Test validator with invalid leap year date"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            validate_datetime_string("2023-02-29T12:00:00")  # 2023 is not a leap year
        assert "Invalid datetime format" in str(exc_info.value)

class TestValidatorIntegration:
    """Integration tests for validators working together"""
    
    def test_all_validators_with_valid_data(self):
        """Test all validators with valid data"""
        # Act & Assert
        assert is_greater_than_zero(1) == 1
        assert is_not_null_or_empty("Test Headline") == "Test Headline"
        assert validate_datetime_string("2024-01-01T12:00:00") == "2024-01-01T12:00:00"
    
    def test_all_validators_with_invalid_data(self):
        """Test all validators with invalid data"""
        # Act & Assert
        with pytest.raises(ValueError):
            is_greater_than_zero(0)
        
        with pytest.raises(ValueError):
            is_not_null_or_empty("")
        
        with pytest.raises(ValueError):
            validate_datetime_string("invalid date")
    
    def test_validator_error_messages_are_descriptive(self):
        """Test that validator error messages are descriptive"""
        # Test is_greater_than_zero error message
        with pytest.raises(ValueError) as exc_info:
            is_greater_than_zero(-5)
        assert "-5 is not valid" in str(exc_info.value)
        
        # Test is_not_null_or_empty error message
        with pytest.raises(ValueError) as exc_info:
            is_not_null_or_empty(None)
        assert "None is null or empty" in str(exc_info.value)
        
        # Test validate_datetime_string error message
        with pytest.raises(ValueError) as exc_info:
            validate_datetime_string("bad date")
        assert "Invalid datetime format" in str(exc_info.value)
        assert "Must be ISO 8601" in str(exc_info.value)
