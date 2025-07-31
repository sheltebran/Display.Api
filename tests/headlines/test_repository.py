import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from features.headlines.repository import (
    add_headline,
    delete_headlines_for_league,
    get_all_headlines
)
from features.headlines.models import HeadlineDto
from datetime import datetime

# Test data
TEST_HEADLINE_DATA = {
    "title": "Test Headline",
    "description": "Test story description",
    "link": "https://example.com/story",
    "pubDate": "Mon, 01 Jan 2024 12:00:00 +0000"
}

TEST_HEADLINE_DATA_INVALID_DATE = {
    "title": "Test Headline",
    "description": "Test story description", 
    "link": "https://example.com/story",
    "pubDate": "Invalid Date Format"
}

@pytest.mark.asyncio
async def test_add_headline_success(mocker):
    """Test successful addition of a headline"""
    # Arrange
    league_id = 1
    expected_headline_id = 123
    
    mock_conn = AsyncMock()
    mock_fetchrow = AsyncMock(return_value={"headline_id": expected_headline_id})
    mock_conn.fetchrow = mock_fetchrow
    mock_conn.close = AsyncMock()
    
    mock_connect = mocker.patch("features.headlines.repository.asyncpg.connect", return_value=mock_conn)
    mock_get_db_config = mocker.patch("features.headlines.repository.get_db_config", return_value={})
    
    # Act
    result = await add_headline(TEST_HEADLINE_DATA, league_id)
    
    # Assert
    assert result == expected_headline_id
    mock_get_db_config.assert_called_once()
    mock_connect.assert_called_once_with(**{})
    mock_fetchrow.assert_called_once()
    mock_conn.close.assert_called_once()
    
    # Verify the SQL query parameters
    call_args = mock_fetchrow.call_args
    assert call_args[0][1] == TEST_HEADLINE_DATA["title"]
    assert call_args[0][2] == TEST_HEADLINE_DATA["description"]
    assert call_args[0][3] == TEST_HEADLINE_DATA["link"]
    assert call_args[0][5] == league_id

@pytest.mark.asyncio
async def test_add_headline_no_result(mocker):
    """Test add headline when database returns no result"""
    # Arrange
    league_id = 1
    
    mock_conn = AsyncMock()
    mock_fetchrow = AsyncMock(return_value=None)
    mock_conn.fetchrow = mock_fetchrow
    mock_conn.close = AsyncMock()
    
    mock_connect = mocker.patch("features.headlines.repository.asyncpg.connect", return_value=mock_conn)
    mock_get_db_config = mocker.patch("features.headlines.repository.get_db_config", return_value={})
    
    # Act
    result = await add_headline(TEST_HEADLINE_DATA, league_id)
    
    # Assert
    assert result == 0
    mock_conn.close.assert_called_once()

@pytest.mark.asyncio
async def test_add_headline_invalid_date_format(mocker):
    """Test add headline with invalid date format"""
    # Arrange
    league_id = 1
    
    mock_conn = AsyncMock()
    mock_connect = mocker.patch("features.headlines.repository.asyncpg.connect", return_value=mock_conn)
    mock_get_db_config = mocker.patch("features.headlines.repository.get_db_config", return_value={})
    
    # Act
    result = await add_headline(TEST_HEADLINE_DATA_INVALID_DATE, league_id)
    
    # Assert
    assert result == 0  # Should return 0 on exception

@pytest.mark.asyncio
async def test_add_headline_database_exception(mocker):
    """Test add headline when database connection fails"""
    # Arrange
    league_id = 1
    
    mock_connect = mocker.patch("features.headlines.repository.asyncpg.connect", side_effect=Exception("Database connection failed"))
    mock_get_db_config = mocker.patch("features.headlines.repository.get_db_config", return_value={})
    
    # Act
    result = await add_headline(TEST_HEADLINE_DATA, league_id)
    
    # Assert
    assert result == 0

@pytest.mark.asyncio
async def test_delete_headlines_for_league_success(mocker):
    """Test successful deletion of headlines for a league"""
    # Arrange
    league_id = 1
    
    mock_conn = AsyncMock()
    mock_execute = AsyncMock(return_value="DELETE 5")  # 5 rows deleted
    mock_conn.execute = mock_execute
    mock_conn.close = AsyncMock()
    
    mock_connect = mocker.patch("features.headlines.repository.asyncpg.connect", return_value=mock_conn)
    mock_get_db_config = mocker.patch("features.headlines.repository.get_db_config", return_value={})
    
    # Act
    result = await delete_headlines_for_league(league_id)
    
    # Assert
    assert result is True
    mock_get_db_config.assert_called_once()
    mock_connect.assert_called_once_with(**{})
    mock_execute.assert_called_once_with("DELETE FROM headlines WHERE league_id = $1;", league_id)
    mock_conn.close.assert_called_once()

@pytest.mark.asyncio
async def test_delete_headlines_for_league_no_rows_deleted(mocker):
    """Test delete headlines when no rows are deleted"""
    # Arrange
    league_id = 999
    
    mock_conn = AsyncMock()
    mock_execute = AsyncMock(return_value="DELETE 0")  # 0 rows deleted
    mock_conn.execute = mock_execute
    mock_conn.close = AsyncMock()
    
    mock_connect = mocker.patch("features.headlines.repository.asyncpg.connect", return_value=mock_conn)
    mock_get_db_config = mocker.patch("features.headlines.repository.get_db_config", return_value={})
    
    # Act
    result = await delete_headlines_for_league(league_id)
    
    # Assert
    assert result is False

@pytest.mark.asyncio
async def test_delete_headlines_for_league_invalid_response(mocker):
    """Test delete headlines with invalid database response"""
    # Arrange
    league_id = 1
    
    mock_conn = AsyncMock()
    mock_execute = AsyncMock(return_value="INVALID RESPONSE")
    mock_conn.execute = mock_execute
    mock_conn.close = AsyncMock()
    
    mock_connect = mocker.patch("features.headlines.repository.asyncpg.connect", return_value=mock_conn)
    mock_get_db_config = mocker.patch("features.headlines.repository.get_db_config", return_value={})
    
    # Act
    result = await delete_headlines_for_league(league_id)
    
    # Assert
    assert result is False

@pytest.mark.asyncio
async def test_get_all_headlines_success(mocker):
    """Test successful retrieval of all headlines for a league"""
    # Arrange
    league_id = 1
    limit = 10
    
    mock_rows = [
        ("Test Headline 1", "Test story 1", "https://example.com/1", datetime(2024, 1, 1), 1),
        ("Test Headline 2", "Test story 2", "https://example.com/2", datetime(2024, 1, 2), 1)
    ]
    
    mock_conn = AsyncMock()
    mock_fetch = AsyncMock(return_value=mock_rows)
    mock_conn.fetch = mock_fetch
    mock_conn.close = AsyncMock()
    
    mock_connect = mocker.patch("features.headlines.repository.asyncpg.connect", return_value=mock_conn)
    mock_get_db_config = mocker.patch("features.headlines.repository.get_db_config", return_value={})
    
    # Act
    result = await get_all_headlines(league_id, limit)
    
    # Assert
    assert len(result) == 2
    assert all(isinstance(headline, HeadlineDto) for headline in result)
    assert result[0].heading == "Test Headline 1"
    assert result[0].league_id == 1
    assert result[1].heading == "Test Headline 2"
    assert result[1].league_id == 1
    
    mock_get_db_config.assert_called_once()
    mock_connect.assert_called_once_with(**{})
    mock_fetch.assert_called_once()
    mock_conn.close.assert_called_once()
    
    # Verify SQL query parameters
    call_args = mock_fetch.call_args
    assert call_args[0][1] == league_id
    assert call_args[0][2] == limit

@pytest.mark.asyncio
async def test_get_all_headlines_empty_result(mocker):
    """Test get all headlines when no headlines found"""
    # Arrange
    league_id = 999
    limit = 10
    
    mock_conn = AsyncMock()
    mock_fetch = AsyncMock(return_value=[])
    mock_conn.fetch = mock_fetch
    mock_conn.close = AsyncMock()
    
    mock_connect = mocker.patch("features.headlines.repository.asyncpg.connect", return_value=mock_conn)
    mock_get_db_config = mocker.patch("features.headlines.repository.get_db_config", return_value={})
    
    # Act
    result = await get_all_headlines(league_id, limit)
    
    # Assert
    assert result == []
    mock_conn.close.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_headlines_none_result(mocker):
    """Test get all headlines when database returns None"""
    # Arrange
    league_id = 1
    limit = 10
    
    mock_conn = AsyncMock()
    mock_fetch = AsyncMock(return_value=None)
    mock_conn.fetch = mock_fetch
    mock_conn.close = AsyncMock()
    
    mock_connect = mocker.patch("features.headlines.repository.asyncpg.connect", return_value=mock_conn)
    mock_get_db_config = mocker.patch("features.headlines.repository.get_db_config", return_value={})
    
    # Act
    result = await get_all_headlines(league_id, limit)
    
    # Assert
    assert result == []

@pytest.mark.asyncio
async def test_get_all_headlines_database_exception(mocker):
    """Test get all headlines when database exception occurs"""
    # Arrange
    league_id = 1
    limit = 10
    
    mock_connect = mocker.patch("features.headlines.repository.asyncpg.connect", side_effect=Exception("Database error"))
    mock_get_db_config = mocker.patch("features.headlines.repository.get_db_config", return_value={})
    
    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await get_all_headlines(league_id, limit)
    
    assert exc_info.value.status_code == 500
    assert "An error occurred while writing" in str(exc_info.value.detail)
