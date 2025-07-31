import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from features.headlines.services import (
    create_headlines_for_sport, 
    get_headlines_by_league, 
    import_headlines
)
from features.headlines.models import HeadlineDto
from datetime import datetime

# Test data
TEST_LEAGUE_DATA = [
    {"league_id": 1, "url": "https://example.com/rss1"},
    {"league_id": 2, "url": "https://example.com/rss2"}
]

TEST_HEADLINES_DATA = [
    {
        "title": "Test Headline 1",
        "description": "Test story 1",
        "link": "https://example.com/story1",
        "pubDate": "Mon, 01 Jan 2024 12:00:00 +0000"
    },
    {
        "title": "Test Headline 2", 
        "description": "Test story 2",
        "link": "https://example.com/story2",
        "pubDate": "Tue, 02 Jan 2024 12:00:00 +0000"
    }
]

TEST_HEADLINE_DTOS = [
    HeadlineDto(
        heading="Test Headline 1",
        story="Test story 1", 
        link="https://example.com/story1",
        pub_date=datetime(2024, 1, 1, 12, 0, 0),
        league_id=1
    ),
    HeadlineDto(
        heading="Test Headline 2",
        story="Test story 2",
        link="https://example.com/story2", 
        pub_date=datetime(2024, 1, 2, 12, 0, 0),
        league_id=1
    )
]

@pytest.mark.asyncio
async def test_create_headlines_for_sport_success(mocker):
    """Test successful creation of headlines for a sport"""
    # Arrange
    sport_id = 1
    mock_get_leagues = mocker.patch("features.headlines.services.get_leagues", return_value=TEST_LEAGUE_DATA)
    mock_import_headlines = mocker.patch("features.headlines.services.import_headlines", return_value=TEST_HEADLINES_DATA)
    mock_delete_headlines = mocker.patch("features.headlines.services.delete_headlines_for_league", return_value=True)
    mock_add_headline = mocker.patch("features.headlines.services.add_headline", return_value=1)
    
    # Act
    await create_headlines_for_sport(sport_id)
    
    # Assert
    mock_get_leagues.assert_called_once_with(sport_id)
    assert mock_import_headlines.call_count == 2  # Two leagues
    assert mock_delete_headlines.call_count == 2  # Two leagues
    assert mock_add_headline.call_count == 4  # Two headlines per league

@pytest.mark.asyncio
async def test_create_headlines_for_sport_no_leagues(mocker):
    """Test create headlines when no leagues found for sport"""
    # Arrange
    sport_id = 999
    mock_get_leagues = mocker.patch("features.headlines.services.get_leagues", return_value=None)
    
    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await create_headlines_for_sport(sport_id)
    
    assert exc_info.value.status_code == 404
    assert f"No leagues found for sport {sport_id}" in str(exc_info.value.detail)
    mock_get_leagues.assert_called_once_with(sport_id)

@pytest.mark.asyncio
async def test_create_headlines_for_sport_no_headlines_for_league(mocker):
    """Test create headlines when no headlines found for a league"""
    # Arrange
    sport_id = 1
    mock_get_leagues = mocker.patch("features.headlines.services.get_leagues", return_value=TEST_LEAGUE_DATA[:1])
    mock_import_headlines = mocker.patch("features.headlines.services.import_headlines", return_value=None)
    
    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await create_headlines_for_sport(sport_id)
    
    assert exc_info.value.status_code == 404
    assert f"No headlines found for league {TEST_LEAGUE_DATA[0]['league_id']}" in str(exc_info.value.detail)

@pytest.mark.asyncio
async def test_create_headlines_for_sport_add_headline_fails(mocker):
    """Test create headlines when adding headline to database fails"""
    # Arrange
    sport_id = 1
    mock_get_leagues = mocker.patch("features.headlines.services.get_leagues", return_value=TEST_LEAGUE_DATA[:1])
    mock_import_headlines = mocker.patch("features.headlines.services.import_headlines", return_value=TEST_HEADLINES_DATA[:1])
    mock_delete_headlines = mocker.patch("features.headlines.services.delete_headlines_for_league", return_value=True)
    mock_add_headline = mocker.patch("features.headlines.services.add_headline", return_value=None)
    
    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await create_headlines_for_sport(sport_id)
    
    assert exc_info.value.status_code == 500
    assert "Failed to add headline to database" in str(exc_info.value.detail)

@pytest.mark.asyncio
async def test_get_headlines_by_league_success(mocker):
    """Test successful retrieval of headlines by league"""
    # Arrange
    league_id = 1
    limit = 10
    mock_get_all_headlines = mocker.patch("features.headlines.services.get_all_headlines", return_value=TEST_HEADLINE_DTOS)
    
    # Act
    result = await get_headlines_by_league(league_id, limit)
    
    # Assert
    mock_get_all_headlines.assert_called_once_with(league_id, limit)
    assert result == TEST_HEADLINE_DTOS
    assert len(result) == 2

@pytest.mark.asyncio
async def test_get_headlines_by_league_default_limit(mocker):
    """Test get headlines by league with default limit"""
    # Arrange
    league_id = 1
    mock_get_all_headlines = mocker.patch("features.headlines.services.get_all_headlines", return_value=TEST_HEADLINE_DTOS)
    
    # Act
    result = await get_headlines_by_league(league_id)
    
    # Assert
    mock_get_all_headlines.assert_called_once_with(league_id, 10)  # Default limit
    assert result == TEST_HEADLINE_DTOS

@pytest.mark.asyncio
async def test_get_headlines_by_league_empty_result(mocker):
    """Test get headlines by league when no headlines found"""
    # Arrange
    league_id = 999
    limit = 10
    mock_get_all_headlines = mocker.patch("features.headlines.services.get_all_headlines", return_value=[])
    
    # Act
    result = await get_headlines_by_league(league_id, limit)
    
    # Assert
    mock_get_all_headlines.assert_called_once_with(league_id, limit)
    assert result == []

@pytest.mark.asyncio
async def test_import_headlines_success(mocker):
    """Test successful import of headlines from RSS feed"""
    # Arrange
    url = "https://example.com/rss"
    mock_fetch_external_data = mocker.patch("features.headlines.services.fetch_external_data", return_value=TEST_HEADLINES_DATA)
    
    # Act
    result = await import_headlines(url)
    
    # Assert
    mock_fetch_external_data.assert_called_once_with(url)
    assert result == TEST_HEADLINES_DATA
    assert len(result) == 2

@pytest.mark.asyncio
async def test_import_headlines_empty_feed(mocker):
    """Test import headlines when RSS feed is empty"""
    # Arrange
    url = "https://example.com/empty-rss"
    mock_fetch_external_data = mocker.patch("features.headlines.services.fetch_external_data", return_value=[])
    
    # Act
    result = await import_headlines(url)
    
    # Assert
    mock_fetch_external_data.assert_called_once_with(url)
    assert result == []

@pytest.mark.asyncio
async def test_import_headlines_none_result(mocker):
    """Test import headlines when fetch returns None"""
    # Arrange
    url = "https://example.com/invalid-rss"
    mock_fetch_external_data = mocker.patch("features.headlines.services.fetch_external_data", return_value=None)
    
    # Act
    result = await import_headlines(url)
    
    # Assert
    mock_fetch_external_data.assert_called_once_with(url)
    assert result is None

@pytest.mark.asyncio
async def test_create_headlines_for_sport_integration_flow(mocker):
    """Test the complete integration flow of create_headlines_for_sport"""
    # Arrange
    sport_id = 1
    mock_get_leagues = mocker.patch("features.headlines.services.get_leagues", return_value=TEST_LEAGUE_DATA)
    mock_import_headlines = mocker.patch("features.headlines.services.import_headlines", return_value=TEST_HEADLINES_DATA)
    mock_delete_headlines = mocker.patch("features.headlines.services.delete_headlines_for_league", return_value=True)
    mock_add_headline = mocker.patch("features.headlines.services.add_headline", return_value=1)
    
    # Act
    await create_headlines_for_sport(sport_id)
    
    # Assert - Verify the complete flow
    # 1. Get leagues for sport
    mock_get_leagues.assert_called_once_with(sport_id)
    
    # 2. Import headlines for each league
    expected_import_calls = [mocker.call(league["url"]) for league in TEST_LEAGUE_DATA]
    mock_import_headlines.assert_has_calls(expected_import_calls)
    
    # 3. Delete existing headlines for each league
    expected_delete_calls = [mocker.call(league["league_id"]) for league in TEST_LEAGUE_DATA]
    mock_delete_headlines.assert_has_calls(expected_delete_calls)
    
    # 4. Add new headlines for each league
    expected_add_calls = []
    for league in TEST_LEAGUE_DATA:
        for headline in TEST_HEADLINES_DATA:
            expected_add_calls.append(mocker.call(headline, league["league_id"]))
    mock_add_headline.assert_has_calls(expected_add_calls)
