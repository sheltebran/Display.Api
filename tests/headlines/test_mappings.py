import pytest
from features.headlines.mappings import map_headline_to_dtos
from features.headlines.models import Headline, HeadlineDto
from datetime import datetime

# Test data
TEST_HEADLINES = [
    Headline(
        headline_id=1,
        heading="Test Headline 1",
        story="Test story 1 description",
        link="https://example.com/story1",
        pub_date=datetime(2024, 1, 1, 12, 0, 0),
        league_id=1
    ),
    Headline(
        headline_id=2,
        heading="Test Headline 2",
        story="Test story 2 description",
        link="https://example.com/story2",
        pub_date=datetime(2024, 1, 2, 14, 30, 0),
        league_id=2
    ),
    Headline(
        headline_id=3,
        heading="Test Headline 3",
        story="Test story 3 description",
        link="https://example.com/story3",
        pub_date=datetime(2024, 1, 3, 16, 45, 0),
        league_id=1
    )
]

def test_map_headline_to_dtos_success():
    """Test successful mapping of headlines to DTOs"""
    # Act
    result = map_headline_to_dtos(TEST_HEADLINES)
    
    # Assert
    assert len(result) == 3
    assert all(hasattr(dto, 'heading') and hasattr(dto, 'story') and hasattr(dto, 'league_id') for dto in result)
    
    # Check first headline mapping
    assert result[0].heading == "Test Headline 1"
    assert result[0].story == "Test story 1 description"
    assert result[0].link == "https://example.com/story1"
    assert result[0].pub_date == datetime(2024, 1, 1, 12, 0, 0)
    assert result[0].league_id == 1
    
    # Check second headline mapping
    assert result[1].heading == "Test Headline 2"
    assert result[1].story == "Test story 2 description"
    assert result[1].link == "https://example.com/story2"
    assert result[1].pub_date == datetime(2024, 1, 2, 14, 30, 0)
    assert result[1].league_id == 2
    
    # Check third headline mapping
    assert result[2].heading == "Test Headline 3"
    assert result[2].story == "Test story 3 description"
    assert result[2].link == "https://example.com/story3"
    assert result[2].pub_date == datetime(2024, 1, 3, 16, 45, 0)
    assert result[2].league_id == 1

def test_map_headline_to_dtos_empty_list():
    """Test mapping empty list of headlines"""
    # Act
    result = map_headline_to_dtos([])
    
    # Assert
    assert result == []
    assert isinstance(result, list)

def test_map_headline_to_dtos_single_headline():
    """Test mapping single headline to DTO"""
    # Arrange
    single_headline = [TEST_HEADLINES[0]]
    
    # Act
    result = map_headline_to_dtos(single_headline)
    
    # Assert
    assert len(result) == 1
    assert hasattr(result[0], 'heading') and hasattr(result[0], 'story') and hasattr(result[0], 'league_id')
    assert result[0].heading == "Test Headline 1"
    assert result[0].story == "Test story 1 description"
    assert result[0].link == "https://example.com/story1"
    assert result[0].pub_date == datetime(2024, 1, 1, 12, 0, 0)
    assert result[0].league_id == 1

def test_map_headline_to_dtos_preserves_data_integrity():
    """Test that mapping preserves all data integrity"""
    # Act
    result = map_headline_to_dtos(TEST_HEADLINES)
    
    # Assert - Verify all fields are correctly mapped
    for i, (original, dto) in enumerate(zip(TEST_HEADLINES, result)):
        assert dto.heading == original.heading, f"Heading mismatch at index {i}"
        assert dto.story == original.story, f"Story mismatch at index {i}"
        assert dto.link == original.link, f"Link mismatch at index {i}"
        assert dto.pub_date == original.pub_date, f"Pub date mismatch at index {i}"
        assert dto.league_id == original.league_id, f"League ID mismatch at index {i}"
        
        # Verify that headline_id is NOT included in DTO (as expected)
        assert not hasattr(dto, 'headline_id'), f"DTO should not have headline_id at index {i}"

def test_map_headline_to_dtos_different_leagues():
    """Test mapping headlines from different leagues"""
    # Arrange
    mixed_league_headlines = [TEST_HEADLINES[0], TEST_HEADLINES[1]]  # League 1 and 2
    
    # Act
    result = map_headline_to_dtos(mixed_league_headlines)
    
    # Assert
    assert len(result) == 2
    assert result[0].league_id == 1
    assert result[1].league_id == 2

def test_map_headline_to_dtos_same_league():
    """Test mapping headlines from the same league"""
    # Arrange
    same_league_headlines = [TEST_HEADLINES[0], TEST_HEADLINES[2]]  # Both league 1
    
    # Act
    result = map_headline_to_dtos(same_league_headlines)
    
    # Assert
    assert len(result) == 2
    assert result[0].league_id == 1
    assert result[1].league_id == 1

def test_map_headline_to_dtos_with_special_characters():
    """Test mapping headlines with special characters"""
    # Arrange
    special_headline = Headline(
        headline_id=999,
        heading="Test with 'quotes' & ampersands",
        story="Story with émojis 🏈 and ñ characters",
        link="https://example.com/story?param=value&other=123",
        pub_date=datetime(2024, 12, 25, 23, 59, 59),
        league_id=999
    )
    
    # Act
    result = map_headline_to_dtos([special_headline])
    
    # Assert
    assert len(result) == 1
    assert result[0].heading == "Test with 'quotes' & ampersands"
    assert result[0].story == "Story with émojis 🏈 and ñ characters"
    assert result[0].link == "https://example.com/story?param=value&other=123"
    assert result[0].league_id == 999

def test_map_headline_to_dtos_with_long_content():
    """Test mapping headlines with very long content"""
    # Arrange
    long_content_headline = Headline(
        headline_id=888,
        heading="A" * 200,  # Very long heading
        story="B" * 500,    # Very long story
        link="https://example.com/" + "c" * 100,  # Long URL
        pub_date=datetime(2024, 6, 15, 10, 30, 45),
        league_id=888
    )
    
    # Act
    result = map_headline_to_dtos([long_content_headline])
    
    # Assert
    assert len(result) == 1
    assert len(result[0].heading) == 200
    assert len(result[0].story) == 500
    assert result[0].link.startswith("https://example.com/")
    assert result[0].league_id == 888

def test_map_headline_to_dtos_maintains_order():
    """Test that mapping maintains the original order of headlines"""
    # Arrange
    ordered_headlines = [
        Headline(1, "First", "Story 1", "link1", datetime(2024, 1, 1), 1),
        Headline(2, "Second", "Story 2", "link2", datetime(2024, 1, 2), 1),
        Headline(3, "Third", "Story 3", "link3", datetime(2024, 1, 3), 1)
    ]
    
    # Act
    result = map_headline_to_dtos(ordered_headlines)
    
    # Assert
    assert len(result) == 3
    assert result[0].heading == "First"
    assert result[1].heading == "Second"
    assert result[2].heading == "Third"
