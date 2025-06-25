import pytest
from core.enums import CreatedStatus
from features.leagues.mappings import map_to_created_league
from features.leagues.services import process_league_message

# Example test data
TEST_DATA = {
    "league_id": 1,
    "sport_id": 1,
    "name": "test",
    "url": "https://example.com",
    "status": CreatedStatus.NEW,
    "event_date": "2024-10-10"}

@pytest.mark.asyncio
async def test_process_league_message_from_dict(mocker):
    # Arrange
    TEST_DATA["status"] = CreatedStatus.DELETE
    mock_delete = mocker.patch("features.leagues.services.delete_league", autospec=True)

    # Act
    result = await process_league_message(TEST_DATA)

    # Assert
    mock_delete.assert_called_once_with(TEST_DATA["sport_id"], TEST_DATA["name"])
    assert result == True

@pytest.mark.asyncio
async def test_process_league_message_bad_write(mocker):
    # Arrange
    TEST_DATA["status"] = CreatedStatus.NEW
    mocker.patch("features.leagues.services.delete_league", return_value=True)
    mock_add = mocker.patch("features.leagues.services.add_created_league", return_value=0)

    # Act
    league = map_to_created_league(TEST_DATA)
    result = await process_league_message(TEST_DATA)

    # Assert
    mock_add.assert_called_once_with(league)
    assert result == False

@pytest.mark.asyncio
async def test_process_league_message_successful_write(mocker):
    # Arrange
    mocker.patch("features.leagues.services.delete_league", return_value=True)
    mock_add = mocker.patch("features.leagues.services.add_created_league", return_value=1)

    # Act
    league = map_to_created_league(TEST_DATA)
    result = await process_league_message(TEST_DATA)

    # Assert
    mock_add.assert_called_once_with(league)
    assert result == True
