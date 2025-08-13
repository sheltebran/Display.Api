import pytest
from core.enums import CreatedStatus
from features.leagues.mappings import map_to_created_league
from features.leagues.services import process_league_message

# Example test data
TEST_LEAGUE_DATA = {
    "league_id": 1,
    "sport_id": 1,
    "name": "test",
    "url": "https://example.com",
    "status": CreatedStatus.NEW,
    "event_date": "2024-10-10"}

@pytest.mark.asyncio
async def test_process_league_message_delete_status(mocker):
    # Arrange
    test_data = TEST_LEAGUE_DATA.copy()
    test_data["status"] = CreatedStatus.DELETE
    mock_delete = mocker.patch("features.leagues.services.delete_league", autospec=True)

    # Act
    result = await process_league_message(test_data)

    # Assert
    mock_delete.assert_called_once_with(test_data["sport_id"], test_data["name"])
    assert result == True

@pytest.mark.asyncio
async def test_process_league_message_failed_league_creation(mocker):
    # Arrange
    test_data = TEST_LEAGUE_DATA.copy()
    mock_delete = mocker.patch("features.leagues.services.delete_league", return_value=True)
    mock_add = mocker.patch("features.leagues.services.add_created_league", return_value=0)

    # Act
    league = map_to_created_league(test_data)
    result = await process_league_message(test_data)

    # Assert
    mock_delete.assert_called_once_with(test_data["sport_id"], test_data["name"])
    mock_add.assert_called_once_with(league)
    assert result == False

@pytest.mark.asyncio
async def test_process_league_message_successful_creation(mocker):
    # Arrange
    test_data = TEST_LEAGUE_DATA.copy()
    mock_delete = mocker.patch("features.leagues.services.delete_league", return_value=True)
    mock_add = mocker.patch("features.leagues.services.add_created_league", return_value=1)

    # Act
    league = map_to_created_league(test_data)
    result = await process_league_message(test_data)

    # Assert
    mock_delete.assert_called_once_with(test_data["sport_id"], test_data["name"])
    mock_add.assert_called_once_with(league)
    assert result == True
