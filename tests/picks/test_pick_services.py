import pytest
from core.enums import CreatedStatus, PickWin
from features.picks.mappings import map_to_created_pick, map_to_created_pick_details
from features.picks.services import process_pick_message

# Example test data
TEST_PICK_DATA = {
    "pick_id": 1,
    "bet": 100,
    "amount_won": 0,
    "week_id": 1,
    "user_team_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": CreatedStatus.NEW,
    "event_date": "2024-10-10T12:00:00Z",
    "pick_details": [
        {
            "pick_detail_id": 1,
            "game_id": 101,
            "spread": -3.5,
            "total": 45.5,
            "is_correct": PickWin.NONE,
            "pick_id": 1,
            "football_team_id": "KC"
        },
        {
            "pick_detail_id": 2,
            "game_id": 102,
            "spread": 7.0,
            "total": 52.0,
            "is_correct": PickWin.NONE,
            "pick_id": 1,
            "football_team_id": "BUF"
        }
    ]
}

@pytest.mark.asyncio
async def test_process_pick_message_delete_status(mocker):
    """Test processing a pick message with DELETE status"""
    # Arrange
    test_data = TEST_PICK_DATA.copy()
    test_data["status"] = CreatedStatus.DELETE
    mock_delete = mocker.patch("features.picks.services.delete_pick", autospec=True)
    
    # Act
    result = await process_pick_message(test_data)
    
    # Assert
    mock_delete.assert_called_once_with(test_data["pick_id"], test_data["user_team_id"])
    assert result == True

@pytest.mark.asyncio
async def test_process_pick_message_successful_creation(mocker):
    """Test successful pick message processing with pick details"""
    # Arrange
    test_data = TEST_PICK_DATA.copy()
    mock_delete = mocker.patch("features.picks.services.delete_pick", return_value=True)
    mock_add_pick = mocker.patch("features.picks.services.add_created_pick", return_value=1)
    mock_add_detail = mocker.patch("features.picks.services.add_created_pick_detail", return_value=1)
    
    # Act
    result = await process_pick_message(test_data)
    
    # Assert
    mock_delete.assert_called_once_with(test_data["pick_id"], test_data["user_team_id"])
    mock_add_pick.assert_called_once()
    assert mock_add_detail.call_count == 2  # Two pick details
    assert result == True

@pytest.mark.asyncio
async def test_process_pick_message_failed_pick_creation(mocker):
    """Test pick message processing when pick creation fails"""
    # Arrange
    test_data = TEST_PICK_DATA.copy()
    mock_delete = mocker.patch("features.picks.services.delete_pick", return_value=True)
    mock_add_pick = mocker.patch("features.picks.services.add_created_pick", return_value=0)
    
    # Act
    result = await process_pick_message(test_data)
    
    # Assert
    mock_delete.assert_called_once_with(test_data["pick_id"], test_data["user_team_id"])
    mock_add_pick.assert_called_once()
    assert result == False

@pytest.mark.asyncio
async def test_process_pick_message_no_pick_details(mocker):
    """Test processing a pick message with no pick details"""
    # Arrange
    test_data = TEST_PICK_DATA.copy()
    test_data["pick_details"] = []
    mock_delete = mocker.patch("features.picks.services.delete_pick", return_value=True)
    mock_add_pick = mocker.patch("features.picks.services.add_created_pick", return_value=1)
    mock_add_detail = mocker.patch("features.picks.services.add_created_pick_detail")
    
    # Act
    result = await process_pick_message(test_data)
    
    # Assert
    mock_delete.assert_called_once_with(test_data["pick_id"], test_data["user_team_id"])
    mock_add_pick.assert_called_once()
    mock_add_detail.assert_not_called()
    assert result == True

@pytest.mark.asyncio
async def test_process_pick_message_exception_handling(mocker):
    """Test pick message processing when an exception occurs"""
    # Arrange
    test_data = TEST_PICK_DATA.copy()
    mock_delete = mocker.patch("features.picks.services.delete_pick", side_effect=Exception("Database error"))

    # Act
    result = await process_pick_message(test_data)

    # Assert
    mock_delete.assert_called_once_with(test_data["pick_id"], test_data["user_team_id"])
    assert result == False

def test_map_to_created_pick():
    """Test mapping pick data to CreatedPick object"""
    # Arrange
    test_data = TEST_PICK_DATA.copy()
    
    # Act
    created_pick = map_to_created_pick(test_data)
    
    # Assert
    assert created_pick.pick_id == test_data["pick_id"]
    assert created_pick.bet == test_data["bet"]
    assert created_pick.amount_won == test_data["amount_won"]
    assert created_pick.week_id == test_data["week_id"]
    assert created_pick.user_team_id == test_data["user_team_id"]
    assert created_pick.parlay_size == len(test_data["pick_details"])
    assert created_pick.created_pick_id == 0  # Should be set by database

def test_map_to_created_pick_details():
    """Test mapping pick details data to CreatedPickDetail objects"""
    # Arrange
    test_details = TEST_PICK_DATA["pick_details"]
    created_pick_id = 1
    event_date_str = TEST_PICK_DATA["event_date"]
    
    # Act
    created_pick_details = map_to_created_pick_details(test_details, created_pick_id, event_date_str)
    
    # Assert
    assert len(created_pick_details) == 2
    
    # Check first detail
    detail1 = created_pick_details[0]
    assert detail1.pick_detail_id == test_details[0]["pick_detail_id"]
    assert detail1.game_id == test_details[0]["game_id"]
    assert detail1.spread == float(test_details[0]["spread"])
    assert detail1.total == float(test_details[0]["total"])
    assert detail1.is_correct == test_details[0]["is_correct"]
    assert detail1.created_pick_id == created_pick_id
    assert detail1.football_team_id == test_details[0]["football_team_id"]
    assert detail1.created_pick_detail_id == 0  # Should be set by database
    
    # Check second detail
    detail2 = created_pick_details[1]
    assert detail2.pick_detail_id == test_details[1]["pick_detail_id"]
    assert detail2.game_id == test_details[1]["game_id"]
    assert detail2.spread == float(test_details[1]["spread"])
    assert detail2.total == float(test_details[1]["total"])
    assert detail2.is_correct == test_details[1]["is_correct"]
    assert detail2.created_pick_id == created_pick_id
    assert detail2.football_team_id == test_details[1]["football_team_id"]

def test_map_to_created_pick_empty_details():
    """Test mapping pick data with empty pick details"""
    # Arrange
    test_data = TEST_PICK_DATA.copy()
    test_data["pick_details"] = []
    
    # Act
    created_pick = map_to_created_pick(test_data)
    
    # Assert
    assert created_pick.parlay_size == 0
